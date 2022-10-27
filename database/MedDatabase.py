import sqlite3
from typing import Optional, Dict, List, Union, Literal

from database.entities.Entity import *
from database.entities.Entity import Answer


class QuestionNotFoundError(Exception):
    pass


def _answer_from_response(answer: list) -> Answer:
    return Answer(id_=answer[0], name=answer[1])


def _question_from_response(question: list) -> Question:
    question_ = question[0]
    return Question(id_=question_[0],
                    name=question_[1],
                    short=question_[2],
                    type_=question_[3],
                    require=question_[4],
                    measure=question_[5],
                    private=question_[6],
                    start=question_[7],
                    next_question_id=question_[8],
                    block=question_[9]
                    )


def _list_answers_from_response(answers_list_response: list) -> list[Answer]:
    return list(map(lambda answer: Answer(id_=answer[0],
                                          name=answer[1],
                                          ),
                    answers_list_response))


def _list_question_from_response(questions_list_response: list) -> list[Question]:
    return list(map(lambda question: Question(id_=question[0],
                                              name=question[1],
                                              short=question[2],
                                              type_=question[3],
                                              require=question[4],
                                              measure=question[5],
                                              private=question[6],
                                              start=question[7],
                                              next_question_id=question[8],
                                              block=question[9]
                                              ),
                    questions_list_response))


def _list_patients_from_response(patients_list_response: list) -> list[Patient]:
    return list(map(lambda patient: Patient(id_=patient[0],
                                            name=patient[1],
                                            male=patient[2],
                                            age=patient[3],
                                            ),
                    patients_list_response))


class MedDatabase:
    NAME_DB: str = "./med.db"

    def __init__(self):
        self.create_db()

    def execute(self, script: str, *args, need_answer: bool = False) -> Optional[list]:
        conn = sqlite3.connect(self.NAME_DB)
        cursor = conn.cursor()

        def close():
            conn.commit()
            cursor.close()
            conn.close()

        if args:
            cursor.execute(script, args)
        else:
            cursor.execute(script)

        if need_answer:
            answer: Optional[list] = cursor.fetchall()
            close()
            return answer
        else:
            close()

    def create_db(self):
        self.execute(Patient.CREATE_TABLE)
        self.execute(Answer.CREATE_TABLE)
        self.execute(PatientAnswer.CREATE_TABLE)
        self.execute(Question.CREATE_TABLE)
        self.execute(EnableAnswers.CREATE_TABLE)
        self.execute(BranchQuestions.CREATE_TABLE)
        self.execute(QuestionType.CREATE_TABLE)

        # добавляем ответы Да и Нет с нужными id, если их еще нет в БД
        if not self.execute(Answer.GET_BOOL_ANSWERS, need_answer=True):
            self.execute(Answer.INSERT_BOOL_ANSWER)

        if not self.execute(QuestionType.GET_TYPES, need_answer=True):
            self.execute(QuestionType.INSERT_TYPES)

    def add_patient(self, name: str, age: int, male: int):
        self.execute(Patient.INSERT_ALL, name, age, male)

    def get_count_questions(self) -> int:
        return self.execute(Question.GET_COUNT, need_answer=True)[0][0] + 1

    def _get_id(self, check_query: str, check_field) -> Optional[int]:
        try:
            return self.execute(check_query, check_field, need_answer=True)[0][0]
        except IndexError:
            return None

    def _insert_entity_if_not_exist(self, check_query: str, check_field, insert_query: str, *insert_fields) -> int:
        id_ = self._get_id(check_query, check_field)
        if id_ is None:
            self.execute(insert_query, *insert_fields)
            id_ = self._get_id(check_query, check_field)
        return id_

    def insert_question(self, question: Question):
        question_id = self._insert_entity_if_not_exist(Question.GET_ID_BY_NAME, question.name,
                                                       Question.INSERT,
                                                       question.name, question.short, question.type_, question.measure,
                                                       question.require_int, question.private_int)
        if question.type_ == Question.TypeAnswer.BOOL.value:
            self.execute(EnableAnswers.INSERT_NO_ANSWER, question_id)
            self.execute(EnableAnswers.INSERT_YES_ANSWER, question_id)
        else:
            if question.type_ == Question.TypeAnswer.MANY.value and question.list_answers:
                for answer in question.list_answers:
                    answer_id = self._insert_entity_if_not_exist(Answer.GET_ID_BY_TEXT, answer, Answer.INSERT_INTO,
                                                                 answer)
                    self.execute(EnableAnswers.INSERT_ANSWER, question_id, answer_id)

    def get_question_by_id(self, id_: int) -> Question:
        return _list_question_from_response(self.execute(Question.GET, id_, need_answer=True))[0]

    def get_question_id_by_name(self, name: str) -> Optional[int]:
        id_ = self._get_id(Question.GET_ID_BY_NAME, name)
        return id_

    def get_questions_order(self):
        questions_list = self.execute(Question.SELECT_ALL_ORDER_ASC, need_answer=True)
        return _list_question_from_response(questions_list)

    def get_enable_answers(self, question_id: int) -> list[Answer]:
        return _list_answers_from_response(
            self.execute(EnableAnswers.SELECT_BY_QUESTION_ID, question_id, need_answer=True))

    def update_question(self, question: Question):
        self.execute(Question.UPDATE_QUESTION,
                     question.name,
                     question.short,
                     question.type_,
                     question.measure,
                     question.require_int,
                     question.private_int,
                     question.id_,
                     )
        if question.type_ == Question.TypeAnswer.BOOL.value:
            self.execute(EnableAnswers.INSERT_YES_ANSWER, question.id_)
            self.execute(EnableAnswers.INSERT_NO_ANSWER, question.id_)
        if question.type_ in [Question.TypeAnswer.INTEGER.value, Question.TypeAnswer.TEXT.value,
                              Question.TypeAnswer.FLOAT.value]:
            self.execute(EnableAnswers.DELETE_ANSWERS_FROM_QUESTION, question.id_)
        if question.list_answers:
            self.execute(EnableAnswers.DELETE_ANSWERS_FROM_QUESTION, question.id_)
            for answer in question.list_answers:
                answer_id = self.execute(Answer.GET_ID_BY_TEXT, answer)
                self.execute(EnableAnswers.INSERT_ANSWER, question.id_, answer_id)

    def delete_question(self, question_id: int):
        question = _question_from_response(self.execute(Question.GET, question_id, need_answer=True))
        if question.start != 1:
            prev_question = _question_from_response(self.execute(Question.GET_PREV, question_id, need_answer=True))
        else:
            prev_question = None

        if question.next_question_id != -1:
            next_question = _question_from_response(
                self.execute(Question.GET, question.next_question_id, need_answer=True))
        else:
            next_question = None

        if next_question is None and prev_question is None:
            self.execute(EnableAnswers.DELETE_JUMP, question.id_)

        elif prev_question is None:
            self.execute(Question.UPDATE_SET_NEW_START_AND_NEW_BLOCK, question.block, question.next_question_id)
            self.execute(EnableAnswers.UPDATE_JUMP_QUESTION, question.next_question_id, question.id_)

        elif next_question is None:
            self.execute(Question.SET_STOP_INSTEAD_QUESTION, question.id_)
            self.execute(EnableAnswers.DELETE_JUMP, question.id_)

        else:
            self.execute(Question.UPDATE_NEXT_QUESTION, question.next_question_id, prev_question.id_)

        self.execute(Question.DELETE_BY_ID, question.id_)
        self.execute(EnableAnswers.DELETE_QUESTION, question.id_)

    def get_next_questions(self, question_id: int) -> list[Question]:
        """Return chain next questions with receive question on first position. """

        def gnq(id_: int, acc: list[Question]) -> list[Question]:
            if id_ == -1:
                return acc
            else:
                question_ = _question_from_response(self.execute(Question.GET, id_, need_answer=True))
                acc.append(question_)
                return gnq(question_.next_question_id, acc)

        # question = _list_question_from_response(self.execute(Question.GET, question_id, need_answer=True))[0]
        return gnq(question_id, list())

    def get_jump(self, question_id: int) -> dict[Union[Literal['basic_block'], Answer], list[bool, list[Question]]]:
        """Return dictionary with all variants branch questions, where key is:
             - answer on question for open blocks
             - or "basic_block" for next questions in same block where receive question. """

        def _answer_to_dict(answer_id: Optional[int], answer_name: Optional[str], jump_question_id: Optional[int],
                            cycle: int) -> \
                dict[Answer, list[bool, list[Question]]]:
            """Transformation receive from DB to dictionary."""
            if jump_question_id is None:
                return {Answer(answer_id, answer_name): [False, list()]}
            elif answer_id is None or answer_name is None:
                return {NoAnswer: [bool(cycle), self.get_next_questions(jump_question_id)]}
            else:
                return {Answer(answer_id, answer_name): [bool(cycle), self.get_next_questions(jump_question_id)]}

        question = _question_from_response(self.execute(Question.GET, question_id, need_answer=True))
        return_dict = {}
        question_branch = self.execute(EnableAnswers.SELECT_CYCLE_BY_QUESTION_ID, question.id_, need_answer=True)
        # добавляем доступные вопросы при различных ответах
        for branch in question_branch:
            return_dict.update(_answer_to_dict(*branch))

        # добавляем вопросы, котороые идут в основном блоке после данного вопроса
        return_dict["basic_block"] = [False, self.get_next_questions(question.next_question_id)]
        return return_dict

    def update_jump(self, question_id: int, answer_id: int, destination_id: int):
        self.execute(EnableAnswers.UPDATE_JUMP, destination_id, question_id, answer_id)

    def get_patients(self) -> list[Patient]:
        return _list_patients_from_response(self.execute(Patient.SELECT_ALL, need_answer=True))

    def delete_patient(self, patient_id: int):
        self.execute(Patient.DELETE, patient_id)

    def add_answer_to_question(self, answer: str, question_id: int) -> int:
        answer_id = self._insert_entity_if_not_exist(Answer.GET_ID_BY_TEXT, answer, Answer.INSERT_INTO, answer)
        self.execute(EnableAnswers.INSERT_ANSWER, question_id, answer_id)
        return answer_id

    def delete_question_with_answer(self, question_id: int, answer_id: int):
        self.execute(EnableAnswers.DELETE_QUESTION_AND_ANSWER, question_id, answer_id)

    def update_cycle(self, question_id: int, answer_id: int, from_: int, to: int, cycle: int):
        if answer_id is None:
            self.execute(EnableAnswers.DELETE_QUESTION_WITH_NONE_ANSWER, question_id)
            self.execute(EnableAnswers.ADD_BRANCH_TO_QUESTION, question_id, from_, cycle)
        else:
            self.execute(EnableAnswers.ADD_JUMP_TO_QUESTION_ANSWER, from_, cycle, question_id, answer_id)
        self.execute(Question.SET_NEW_NEXT_QUESTION, to, question_id)
        self.execute(Question.UPDATE_SET_START, from_)
        self.execute(Question.UPDATE_SET_STOP, to)
        block = int(self.execute(Question.GET_NEXT_BLOCK, need_answer=True)[0][0])
        self._set_new_block(from_, to, block)

    def _set_new_block(self, from_: int, to: int, block: int):
        def snb(id_: int):
            if id_ == -1:
                return
            elif id_ == to:
                self.execute(Question.UPDATE_BLOCK, block, id_)
                return
            else:
                question_ = _question_from_response(self.execute(Question.GET, id_, need_answer=True))
                self.execute(Question.UPDATE_BLOCK, block, id_)
                snb(question_.next_question_id)
        snb(from_)

    def update_next_question(self, old_question_id: int, new_question_id: int):
        self.execute(Question.UPDATE_NEXT_QUESTION, new_question_id, old_question_id)

    def set_start_question(self, question_id: int):
        self.execute(Question.SET_START, question_id)

    def get_last_question(self, block: int) -> Question:
        try:
            return _question_from_response(self.execute(Question.GET_LAST, block, need_answer=True))
        except IndexError:
            raise QuestionNotFoundError()

    def delete_branch(self, question: Question, answer_id: int):
        if answer_id is None:
            first_question_in_branch = _question_from_response(
                self.execute(EnableAnswers.GET_JUMP_BY_QUESTION_WITH_NONE_ANSWER, question.id_, need_answer=True))
            self.execute(EnableAnswers.DELETE_QUESTION_WITH_NONE_ANSWER, question.id_)
        else:
            first_question_in_branch = _question_from_response(
                self.execute(EnableAnswers.GET_JUMP_BY_QUESTION_AND_ANSWER, question.id_, answer_id, need_answer=True))
            self.execute(EnableAnswers.SET_NULL_JUMP, question.id_, answer_id)
        last_question_in_branch = self.get_next_questions(first_question_in_branch.id_)[-1]
        question_after_block = question.next_question_id
        self.execute(Question.UPDATE_NEXT_QUESTION, first_question_in_branch.id_, question.id_)
        self.execute(Question.UPDATE_BLOCK_AND_SET_START_ZERO, question.block, first_question_in_branch.id_)
        self.execute(Question.UPDATE_BLOCK_AND_SET_NEXT_QUESTION, question.block, question_after_block,
                     last_question_in_branch.id_)

    def set_prev_question(self, set_prev_question_id: int, current_question: Question):
        if set_prev_question_id == current_question.id_: return
        set_prev_question = _question_from_response(self.execute(Question.GET, set_prev_question_id, need_answer=True))
        current_prev_question = _question_from_response(self.execute(Question.GET_PREV, current_question.id_, need_answer=True))
        self.execute(Question.UPDATE_SET_START_NEXT_AND_BLOCK, current_question.start, current_question.next_question_id, current_question.block, current_prev_question.id_)
        self.execute(Question.UPDATE_NEXT_QUESTION, current_question.id_, set_prev_question.id_)
        self.execute(Question.UPDATE_SET_NEXT_AND_BLOCK, set_prev_question.next_question_id, set_prev_question.block,
                     current_question.id_)


if __name__ == "__main__":
    MedDatabase().add_patient("Ваня", 22, 0)
