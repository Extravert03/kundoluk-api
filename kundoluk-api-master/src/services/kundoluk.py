import contextlib
import itertools
from typing import Optional

import httpx
from bs4 import BeautifulSoup

from exceptions import UnsuccessfulAuthenticationError
from schemas import AuthCredentials, JournalMarks, JournalMarksRow

user_agent = 'Kundoluk-API by usbtypec'


class JournalParser:

    def __init__(self, html: str, student_kundoluk_id: int, lesson_kundoluk_id: int):
        self._soup = BeautifulSoup(html, 'lxml')
        self._student_kundoluk_id = student_kundoluk_id
        self._lesson_kundoluk_id = lesson_kundoluk_id

    def parse_html(self) -> JournalMarks:
        marks_rows = self.__extract_marks_rows()
        average_mark = self.__extract_average_mark()
        student_name = self.__extract_student_name()
        return JournalMarks(mark_rows=marks_rows, average=average_mark,
                            student_id=self._student_kundoluk_id,
                            lesson_id=self._lesson_kundoluk_id,
                            student_name=student_name)

    def __parse_marks_row(self, tds: list[BeautifulSoup]) -> list[JournalMarksRow]:
        results = list()
        with contextlib.suppress(AttributeError):
            mark_date = tds[1].text.replace('\t\t\t\t\t\t\t\r\n\t\t\t\t\t\t\t\t', ' ').replace(
                '\r\n\t\t\t\t\t\t\t', '')
            if len(mark_date.split(' ')) != 2:
                mark_date = ' '.join(mark_date.split(' ')[:2])
            student_work_icon = tds[-2].find("i")
            mark_spans = tds[-1].find_all("span")
            if not mark_spans:
                return results
            for span in mark_spans:
                mark_value = span.text
                mark_caption = span.get("data-uk-tooltip")
                results.append(JournalMarksRow(
                    date=mark_date,
                    mark=mark_value,
                    caption=mark_caption,
                    has_attached_homework=bool(student_work_icon))
                )
        return results

    def __extract_marks_rows(self) -> tuple[JournalMarksRow, ...]:
        try:
            marks_table_rows = self._soup.find("tbody").find_all("tr")
            tds_list = [tr.find_all("td") for tr in marks_table_rows]
        except AttributeError:
            return tuple()
        else:
            nested_marks_info = (self.__parse_marks_row(tds) for tds in tds_list)
            flatten_marks = itertools.chain.from_iterable(nested_marks_info)
            return tuple(flatten_marks)

    def __extract_average_mark(self) -> Optional[str]:
        with contextlib.suppress(AttributeError):
            return self._soup.find("div", class_="average").find("span").text or None

    def __extract_student_name(self) -> str:
        return self._soup.find('div', class_='name').text.strip()


async def get_auth_cookies(auth_credentials: AuthCredentials) -> dict:
    headers = {'user-agent': user_agent}
    data = auth_credentials.dict() | {'language': 'ru'}
    async with httpx.AsyncClient() as client:
        response: httpx.Response = await client.post(
            'https://kundoluk.edu.kg/account/login', data=data, headers=headers)
        if response.status_code != 302:
            raise UnsuccessfulAuthenticationError
        return dict(client.cookies)


async def get_student_grades_by_lesson(cookies: dict, student_id: int,
                                       lesson_id: int, quarter: int) -> JournalMarks:
    url = f'https://kundoluk.edu.kg/journal/student/{student_id}/{lesson_id}'
    async with httpx.AsyncClient(cookies=cookies) as client:
        response = await client.get(url, params={'quarter': quarter})
        return JournalParser(response.text, student_id, lesson_id).parse_html()
