from _typeshed import Incomplete
from abc import ABC
from enum import Enum
from typing import Callable, Iterator
from virtualitics_sdk.elements.dashboard import Dashboard as Dashboard, Row as Row
from virtualitics_sdk.elements.data_source import DataSource as DataSource
from virtualitics_sdk.elements.dropdown import Dropdown as Dropdown
from virtualitics_sdk.elements.element import Element as Element, InputElement as InputElement
from virtualitics_sdk.elements.infograph import Infographic as Infographic
from virtualitics_sdk.page.card import Card as Card
from virtualitics_sdk.page.section import Section as Section

class PageType(Enum):
    INPUT: str
    DATA_LAB: str
    RESULTS: str

class Page(ABC):
    '''The Page for a Step.

    :param title: The title of the Page.
    :param sections: The sections contained inside the Page.
    
    **EXAMPLE:**

       .. code-block:: python

           # Imports 
           from virtualitics_sdk import Page, Section
           . . .
           # Example usage 
           class ExStep(Step):
               def run(self, flow_metadata):
                    . . . 
           ex_step_page = Page(title="Example Page", 
                               sections=[Section("", [])])
           ex_step = ExStep(title="Example", 
                            description="",
                            parent="Data & Visualizations", 
                            type=StepType.RESULTS, 
                            page=ex_step_page)
    '''
    title: Incomplete
    section_map: dict[str, Section]
    virtualitics_sdk_sdk_version: Incomplete
    def __init__(self, title: str, sections: list[Section]) -> None: ...
    @property
    def sections(self) -> list[Section]:
        """Return the sections of a Page.

        :return: The sections on a given Page.
        """
    @property
    def elements(self) -> Iterator[Element]: ...
    @property
    def has_required_input(self) -> bool: ...
    def serialize(self): ...
    def add_card_to_section(self, card: Card, section_title: str):
        """Adds a Card to a specified section.

        :param card: The Card to add.
        :param section_title: The title of the section the Card will be added to.
        :raises ValueError: if no section with that title is found on the page.
        """
    def add_content_to_section(self, elems: Element | list[Element] | list[Row], section_title: str, card_title: str = '', card_subtitle: str = '', card_description: str = '', card_id: str = '', show_card_title: bool = True, show_card_description: bool = True, page_update: Callable | None = None):
        '''Adds content to a section. This adds the specified elements into a single Card on a Section.

        :param elems: The elements to add to the new Card in this Section.
        :param section_title: The title of the section to add elements to.
        :param card_title: The card title for the new card to be added, defaults to "".
        :param card_subtitle: The subtitle for the new card to be added, defaults to "".
        :param card_description: The description for the new card to be added, defaults to "".
        :param card_id: The ID of the new card to be added, defaults to "".
        :param show_card_title: whether to show the title of the card on the page when rendered, defaults to True.
        :param show_card_description: whether to show the description of the card to the page when rendered, defaults to True.
        :param page_update: The page update function for the new card, defaults to None.
        :raises ValueError: if the section title is not found on the Page.
        '''
    def replace_content_in_section(self, elems: Element | list[Element] | list[Row], section_title: str, card_title: str, card_subtitle: str = '', card_description: str = '', show_card_title: bool = True, show_card_description: bool = True, page_update: Callable | None = None, filter_update: Callable | None = None):
        '''Replaces the content on a card with new content. If that card doesn\'t exist, it will add the card to the section.
        It\'s highly recommended to use this function inside of page updates because no matter how many times the page
        is updated, only one card will be shown.

        :param elems: The elements to replace the card with
        :param section_title: The title of the section the new card should exist in
        :param card_title: The title of the card
        :param card_subtitle: The subtitle of the card, defaults to ""
        :param card_description: The description of the card, defaults to ""
        :param show_card_title: whether to show the title of the card on the page when rendered, defaults to True
        :param show_card_description: whether to show the description of the card to the page when rendered, defaults to True
        :param page_update: The page update function for the new card, defaults to None.
        :param filter_update: The filter update function for the new card, defaults to None.
        '''
    def remove_card(self, section_title: str, card_title: str):
        """Remove a card from a Page. This can be called inside dynamic pages to restructure a Page.
        If no card exists with that title, the page will not be changed and this function will not error.

        :param section_title: The section on the page where the Card should be removed
        :param card_title: The title of the Card to be removed
        :raises ValueError: If the section title does not exist on the pageQ
        """
    def get_section_by_title(self, section_title: str) -> Section:
        """Returns the first Section on a Page with a specified title.

        :param section_title: The title of the section to retrieve.
        :raises ValueError: if no section exists with the specified title.
        """
    def get_element_by_title(self, elem_title: str, quiet: bool = False) -> Element:
        """Returns the first Element on a Page with a specified title.

        :param elem_title: The title of the section to retrieve.
        :param quiet: If True, return None if element is not found. Defaults to False
        :raises ValueError: if no element exists with the specified title.
        """
    def get_element_by_id(self, elem_id: str) -> Element:
        """Returns the Element on a Page with a specified ID.

        :param elem_id: The title of the element.
        :raises ValueError: if no element exists with the specified title.
        """
    def get_card_by_id(self, card_id: str) -> Card:
        """Returns the Card on a Page with a specified ID.

        :param card_id: The ID of the card.
        :raises CardNotFoundException: if no card exists with the specified ID.
        """
    def get_card_by_title(self, card_title: str, quiet: bool = False) -> Card:
        """Returns the Element on a Page with a specified ID.

        :param card_title: The title of the card.
        :param quiet: If True, return None if Card is not found. Defaults to False
        :raises CardNotFoundException: if no card exists with the specified title and quiet is False.
        """
    def update_card_title(self, new_card_title: str, card_title: str | None = None, card_id: str | None = None):
        """Update the title of card using the card_title or the card_id

        :param new_card_title: The new title of the card.
        :param card_title: The title of the card, defaults to None.
        :param card_id: The ID of the card, defaults to None.
        :raises PredictException: If card_title or card_id are not specified.
        :raises CardNotFoundException: if no card exists with the specified title or ID.
        """
