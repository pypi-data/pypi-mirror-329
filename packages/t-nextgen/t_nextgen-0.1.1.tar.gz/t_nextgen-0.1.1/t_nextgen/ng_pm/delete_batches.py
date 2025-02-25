import contextlib
import _ctypes
import time

from t_nextgen.ng_pm.core import NextGenPMCore
from t_nextgen.utils.logger import logger


def wait_for_batches_to_be_deleted(
    next_gen: NextGenPMCore, descriptions: list[str], timeout: int = 300, interval: int = 10
) -> None:
    """Waits for the batches to be deleted.

    Args:
        next_gen (NextGenPMCore): NextGen PM Core object.
        descriptions (list[str]): List of batch descriptions to wait for deletion.
        timeout (int): Maximum time to wait for deletion in seconds. Defaults to 300 seconds.
        interval (int): Time interval between checks in seconds. Defaults to 10 seconds.
    """
    logger.info("Waiting for batches to be deleted")
    start_time = time.time()
    while time.time() - start_time < timeout:
        found_batch = False
        pane = next_gen.desktop_app.dialog.child_window(title="lstListing", control_type="Pane")
        data_items = pane.descendants(control_type="DataItem")
        for data_item in data_items:
            description = data_item.descendants(title="Description", control_type="Edit")[0].get_value()
            if any(desc in description for desc in descriptions):
                found_batch = True
                break
        if not found_batch:
            logger.info("All batches have been deleted.")
            return
        logger.info("Batches still found. Waiting...")
        time.sleep(interval)
    logger.warning("Timeout reached. Some batches may not have been deleted.")


def delete_batches(next_gen: NextGenPMCore, batches_to_delete: list[dict]):
    """Deletes batches from the NextGen PM application.

    Args:
        next_gen (NextGenPMCore): NextGen PM Core object.
        batches_to_delete (list[dict]): List of dictionaries containing practice name and descriptions to delete.

    Example:
        batches_to_delete =[
            {
                "practice": "Proliance Southwest Seattle Orthopedics",
                "descriptions": [
                    "*****",
                    "******",
                    "******",
                ]
            },
            {
                "practice": "Proliance Hand Wrist & Elbow Physicians",
                "descriptions": [
                    "*******",
                    "*******",
                    "*****",
                ]
            }
    """
    next_gen.login()
    for batches in batches_to_delete:
        batches_not_secured_to_thoughtful = []
        number_of_remits = 0
        found_batch_to_delete = False
        logger.info(f"Selecting practice: {batches['practice']}")
        next_gen.select_practice_from_app(batches["practice"])

        next_gen.batch_posting_window.click_batch_icon_from_bar(batches["practice"])
        pane = next_gen.desktop_app.dialog.child_window(title="lstListing", control_type="Pane")
        data_items = pane.descendants(control_type="DataItem")

        logger.info(f"Searching for batches to delete in {batches['practice']}")
        for index, data_item in enumerate(data_items):
            description = data_item.descendants(title="Description", control_type="Edit")[0].get_value()
            secured_to = data_item.descendants(title="Secured To", control_type="Edit")[0].get_value()
            if any(desc in description for desc in batches["descriptions"]):

                if not data_item.is_visible():
                    next_gen.desktop_app.click_down_n_times(index)
                with contextlib.suppress(_ctypes.COMError):
                    if "thoughtful" in secured_to.lower():
                        number_of_remits += int(
                            data_item.descendants(title="Members", control_type="Edit")[0].get_value()
                        )
                        found_batch_to_delete = True
                        logger.info(f"Selecting batch for deletion: {description}")
                        data_item.descendants(control_type="CheckBox")[0].toggle()
                    else:
                        batches_not_secured_to_thoughtful.append(description)
                        logger.warning(f"Batch {description} is not secured to Thoughtful. Not marking it to delete")
        if found_batch_to_delete:
            logger.info(f"Deleting {number_of_remits} remits from {batches['practice']}")
            next_gen.batch_posting_window.click_menu_icon("d")
            time.sleep(2)
            with contextlib.suppress(_ctypes.COMError):
                next_gen.desktop_app.dialog.child_window(title="OK", control_type="Button").click()
            wait_for_batches_to_be_deleted(
                next_gen, batches["descriptions"], timeout=number_of_remits * 30, interval=10
            )
        if batches_not_secured_to_thoughtful:
            logger.warning(
                "Some of the batches passed to delete were not secured to thoughtful users. They were not  "
                f"selected to be deleted.Batches not secured to Thoughtful: {batches_not_secured_to_thoughtful}."
            )
        if not found_batch_to_delete and not batches_not_secured_to_thoughtful:
            logger.info(f"No batches found to delete in {batches['practice']}")

    if next_gen_process := next_gen.desktop_app.get_app_session_if_running(next_gen.app_path):
        logger.debug("Closing the NextGen process.")
        next_gen.close_session(next_gen_process)


if __name__ == "__main__":
    batches_to_delete = [
        {
            "practice": "Proliance Southwest Seattle Orthopedics",
            "descriptions": ["*******", "*******", "********"],
        },
    ]
    next_gen = NextGenPMCore()
    delete_batches(next_gen, batches_to_delete)
