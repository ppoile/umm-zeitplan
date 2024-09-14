from datetime import datetime, timedelta
import logging
import os
import pandas
import re


logger = logging.getLogger('zeitplan')


def setup_logging(verbose):
    log_level = logging.INFO
    if verbose:
        log_level=logging.DEBUG
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch = logging.StreamHandler()
    ch.setLevel(log_level)
    ch.setFormatter(formatter)
    root_logger.addHandler(ch)


class Zeitplan(object):
    _eventToColorMapping = {
        # Saturday:
        "U12W": "orange",
        "U12M": "yellow",
        "U16W": "pink",
        "U16M": "cyan",
        # Sunday:
        "U14W": "orange",
        "U14M": "yellow",
        "WOM_5K": "pink",
        "MAN_6K": "cyan",
        # Saturday & Sunday:
        "WOM_7K": "green",
        "MAN_10K": "red",
        "U18M_10K": "darkblue",
    }

    def __init__(self, tasks, resources):
        self._tasks = tasks
        self._resources = resources

    def getTasks(self, resource_name):
        tasks = []
        column_index = self._resources.index(resource_name)
        for task in self._tasks:
            if task[1] == resource_name:
                tasks.append((task, column_index, self.getColorFromEvent(task[0])))
        return tasks

    def getColorFromEvent(self, eventName):
        for k, v in self._eventToColorMapping.items():
            if eventName.startswith(k):
                return v
        return self._eventToColorMapping[eventName]


def main(solution_file, event_name, event_day, start_time):
    logger.debug("main(solution_file={}, event_name={}, event_day={}, start_time={})".format(
        solution_file, event_name, event_day, start_time))
    contentAsString = solution_file.read()
    #print("content: {!r}".format(contentAsString))

    withoutBrackets = contentAsString[1:-1]
    #print("without-brackets: {!r}".format(withoutBrackets))
    tasksAsStrings = withoutBrackets.split("), (")
    tasksAsStrings[0] = tasksAsStrings[0][1:]
    tasksAsStrings[-1] = tasksAsStrings[-1][:-1]
    #print("tasks: {!r}".format(tasksAsStrings))
    tasks = []
    for taskAsString in tasksAsStrings:
        parts = taskAsString.split(', ')
        tasks.append((parts[0], parts[1], int(parts[2]), int(parts[3])))
    #print("tasks: {!r}".format(tasks))

    resources = ["Läufe", "Weit1", "Weit2", "Weit3", "Hoch1", "Hoch2", "Kugel1", "Kugel2", "Kugel3", "Diskus", "Speer", "Stab"]

    zeitplan = Zeitplan(tasks, resources)

    directory, filename = os.path.split(solution_file.name)
    match = re.search(r'(.*)_solution.txt$', filename)
    filename_base = match.group(1)
    filename = filename_base + '_zeitplan.xlsx'
    path = os.path.join(directory, filename)
    writer = pandas.ExcelWriter(path, engine='xlsxwriter')
    workbook = writer.book
    worksheet = workbook.add_worksheet(event_day)

    title_cell_format = workbook.add_format()
    title_cell_format.set_font_size(14)
    title_cell_format.set_bold()
    title_fields = ['Zeitplan']
    if event_name:
        title_fields.append(event_name)
    if event_day:
        title_fields.append(event_day)
    title = ' '.join(title_fields)
    logger.debug("worksheet-1: {}: '{}'".format('A1', title))
    worksheet.write('A1', title, title_cell_format)

    heading_cell_format = workbook.add_format()
    heading_cell_format.set_bold()
    heading_cell_format.set_border()

    empty_table_cell_format = workbook.add_format()
    empty_table_cell_format.set_border()

    def get_time(row_index):
        if start_time is None:
            return str(row_index)
        ts_start = datetime.strptime(start_time, "%H:%M")
        ts_end = ts_start + timedelta(minutes=10*row_index)
        return ts_end.time().strftime("%-H:%M")

    column_index = 0
    for resource in resources:
        logger.debug("column_index={}, resource={}".format(column_index, resource))
        tasks = zeitplan.getTasks(resource)
        if resource == "Läufe":
            first_task = tasks[0][0][2]
            last_task = tasks[-1][0][3] - 2
            logger.debug("worksheet-2: {}/{}: '{}'".format(2, 0, 'Zeit'))
            worksheet.write(2, 0, 'Zeit', heading_cell_format)
            for row_index in range(first_task, last_task + 1):
                logger.debug("worksheet-3: {}/{}: '{}'".format(row_index + 3, column_index, get_time(row_index)))
                worksheet.write(row_index + 3, column_index, get_time(row_index), empty_table_cell_format)
            column_index += 1
        filled_slots = []
        for task_index, task in enumerate(tasks):
            logger.debug("task: {}".format(task))
            logger.debug("worksheet-4: {}/{}: '{}'".format(2, column_index, resource))
            worksheet.write(2, column_index, resource, heading_cell_format)
            color = task[2]
            task_name = task[0][0]
            start_time = task[0][2]
            end_time = task[0][3]
            cell_format = workbook.add_format()
            cell_format.set_pattern(1)
            cell_format.set_border()
            cell_format.set_bg_color(color)
            fields = task_name.split('_')
            find_string_begin = '_'.join(fields[:2])
            find_string_end = fields[-1]
            correct_end_time = True
            if resource == 'Läufe':
                try:
                    next_task_name = tasks[task_index + 1][0][0]
                    if next_task_name.startswith(find_string_begin) and next_task_name.endswith(find_string_end):
                        correct_end_time = False
                except IndexError:
                    pass

            if correct_end_time:
                end_time -= 1

            for row_index in range(start_time, end_time):
                content = ''
                if row_index == start_time:
                    content = task[0][0]
                    if resource != "Läufe":
                        content = content.split('_')[-2]
                logger.debug("worksheet-5: {}/{}: '{}' ({})".format(row_index + 3, column_index, content, color))
                worksheet.write(row_index + 3, column_index, content, cell_format)
                filled_slots.append(row_index)
        if filled_slots:
            for row_index in range(first_task, last_task + 1):
                if row_index not in filled_slots:
                    logger.debug("worksheet-6: {}/{}: '{}'".format(row_index + 3, column_index, ''))
                    worksheet.write(row_index + 3, column_index, '', empty_table_cell_format)
            column_index += 1
    writer.close()


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='generate xlsx zeitplan')
    parser.add_argument('-v', '--verbose', action="store_true", help="be verbose")
    parser.add_argument('-e', '--event', help="Event, z.B. 'UMM'")
    parser.add_argument('-d', '--day', help="Wettkampf-Tag, z.B. 'Samstag'")
    parser.add_argument('-s', '--start-time', help="start time, z.B. '8:30'")
    parser.add_argument('file', type=argparse.FileType('r'), help='solution-file')
    args = parser.parse_args()

    setup_logging(args.verbose)

    main(args.file, args.event, args.day, args.start_time)
