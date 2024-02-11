import re
from datetime import datetime

from scrapy import Spider

from players.items import PlayerInfoItem


PLAYER_CARD_XPATH = '//table[@class="infobox vcard"]'
NAME_XPATH = ".//caption/text()"
FULL_NAME_XPATH = './/th[contains(text(), "Full name")]/following-sibling::td/text()'
DOB_ELEMENT_XPATH = './/th[contains(text(), "Date of birth")]/following-sibling::td'
DOB_XPATH = ".//span[@class='bday']/text()"
AGE_TEXT_XPATH = "./span[@class='noprint ForceAgeToShow']/text()"
POB_ELEMENT_XPATH = './/th[contains(text(), "Place of birth")]/following-sibling::td'
POB_XPATH = "string(.)"
POSITIONS_ELEMENT_XPATH = './/th[contains(text(), "Position(s)")]/following-sibling::td'
POSITIONS_XPATH = "string(.)"
CURRENT_CLUB_XPATH = './/th[contains(., "Current team")]/following-sibling::td/a/text()'
NATIONAL_TEAM_XPATH = './/tr[th[contains(text(),"International career")]]/following-sibling::tr[count(th)=1 and count(td)=3][last()]/td[1]/a/text()'
CURRENT_CLUB_STATS_ELEMENTS_XPATH = './/tr[count(th)=1 and count(td)=3 and td[1][contains(., "{club}")]]'
APPEARANCES_XPATH = ".//td[2]/text()"
GOALS_XPATH = ".//td[3]/text()"

AGE_REGEX = r"\(age (\d+)\)"
NON_BREAKING_SPACE = "\xa0"


class WikipediaPlayerInfoSpider(Spider):
    name = "wikipedia_player_info"

    def __init__(self, start_urls=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not start_urls:
            raise ValueError("start_urls must be provided")
        self.start_urls = start_urls

    def parse(self, response):
        current_timestamp = datetime.utcnow().isoformat()

        player_card = response.xpath(PLAYER_CARD_XPATH)
        if not player_card:
            return

        name = self.get_player_name(player_card)
        full_name = self.get_player_full_name(player_card)
        if not full_name:
            full_name = name

        dob_element = player_card.xpath(DOB_ELEMENT_XPATH)
        dob = self.get_player_dob(dob_element)
        if not dob:
            return
        age = self.get_player_age(dob_element)

        pob_element = player_card.xpath(POB_ELEMENT_XPATH)
        city, country = self.get_player_pob(pob_element)

        positions_element = player_card.xpath(POSITIONS_ELEMENT_XPATH)
        positions_list = self.get_player_positions(positions_element)

        current_club = self.get_player_current_club(player_card)

        national_team = self.get_player_national_team(player_card)

        current_club_stats_elements = response.xpath(CURRENT_CLUB_STATS_ELEMENTS_XPATH.format(club=current_club))

        current_club_appearances, current_club_goals = self.get_player_current_club_stats(current_club_stats_elements)

        yield PlayerInfoItem(
            url=response.url,
            name=name,
            full_name=full_name,
            date_of_birth=dob,
            age=age,
            place_of_birth=city,
            country_of_birth=country,
            positions=positions_list,
            current_club=current_club,
            national_team=national_team,
            appearances_in_current_club=current_club_appearances,
            goals_in_current_club=current_club_goals,
            timestamp=current_timestamp,
        )

    @staticmethod
    def get_player_name(player_card):
        return player_card.xpath(NAME_XPATH).get()

    @staticmethod
    def get_player_full_name(player_card):
        return player_card.xpath(FULL_NAME_XPATH).get()

    @staticmethod
    def get_player_dob(dob_element):
        return dob_element.xpath(DOB_XPATH).get()

    @staticmethod
    def get_player_age(dob_element):
        age_text = dob_element.xpath(AGE_TEXT_XPATH).get().replace(NON_BREAKING_SPACE, " ").strip()  # format "(age 30)"
        try:
            return int(re.match(AGE_REGEX, age_text).group(1))
        except AttributeError:
            return None

    @staticmethod
    def get_player_pob(pob_element):
        pob = pob_element.xpath(POB_XPATH).get()  # format "city, country" or "city1, city2, country" or "country"
        if not pob:
            return "", ""
        pob_parts = [p.strip() for p in pob.rsplit(",", 1)]
        if len(pob_parts) == 2:
            return pob_parts
        else:
            return "", pob_parts[0]

    @staticmethod
    def get_player_positions(positions_element):
        positions = positions_element.xpath(
            POSITIONS_XPATH
        ).get()  # format "position1, position2, ..." or "position" or "position1 / position2 / ..." or "position1/position2" or "position1\nposition2\n..."
        if not positions:
            return []
        return [p.strip().lower() for p in re.split(r"[/,]", positions)]

    @staticmethod
    def get_player_current_club(player_card):
        return player_card.xpath(CURRENT_CLUB_XPATH).get()

    @staticmethod
    def get_player_national_team(player_card):
        return player_card.xpath(NATIONAL_TEAM_XPATH).get()

    @staticmethod
    def get_player_current_club_stats(current_club_stats_elements):
        current_club_appearances = 0
        current_club_goals = 0
        for el in current_club_stats_elements:
            appearances = el.xpath(APPEARANCES_XPATH).get()
            goals = el.xpath(GOALS_XPATH).get().replace("(", "").replace(")", "")  # format "(goals)"
            try:
                current_club_appearances += int(appearances)
            except ValueError:
                pass
            try:
                current_club_goals += int(goals)
            except ValueError:
                pass
        return current_club_appearances, current_club_goals
