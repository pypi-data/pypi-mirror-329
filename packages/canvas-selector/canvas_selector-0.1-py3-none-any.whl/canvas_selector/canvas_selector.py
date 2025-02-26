from canvasapi import Canvas
from load_config import API_KEY, API_URL
from tqdm import tqdm
from argparse import Namespace

canvas = Canvas(API_URL, API_KEY)


class options(Namespace):

    def __init__(self,
                 semester=None,
                 course=None,
                 assignment=None,
                 groups=None):
        super().__init__()
        self.course = course
        self.semester = semester
        self.assignment = assignment
        self.groups = groups


def choose_options(args):
    if not args.course:
        args.course = select_course(canvas.get_courses(state='available'),
                                    enrollment_term_id=args.semester)
    else:
        args.course = canvas.get_course(args.course)

    try:
        if args.groups:
            args.group = choose_one(args.course.get_group_categories())
    except AttributeError:
        args.group = None
        pass

    try:
        if args.assignment:
            asses = args.course.get_assignments(include="assignment")
            asses = choose_many(asses, obj="assignment")
            args.asses = [args.course.get_assignment(x)
                          for x in asses]
    except AttributeError:
        args.asses = []
        pass

    return args


def select_course(courseList, enrollment_term_id=None):

    if enrollment_term_id:
        courses = [course for course in courseList
                   if enrollment_term_id in course.name]
    else:
        courses = courseList

    answers = choose_one(courses, obj="course")

    return answers


def choose_many(pagList, obj="course"):
    from inquirer import Checkbox, prompt

    questions = [Checkbox(obj, message=f" Which {obj} do you want to use? \
(<up>/<down> to navigate, \
<space> to check/uncheck, \
<enter> to confirm)", choices=pagList)]

    answers = prompt(questions)

    return answers[obj]


def choose_one(pagList, obj="course"):
    from inquirer import List, prompt

    questions = [List(obj, message=f" Which {obj} do you want to use? \
(<up>/<down> to navigate, \
<space> to check/uncheck, \
<enter> to confirm)", choices=pagList)]

    answers = prompt(questions)

    return answers[obj]


def mkdir(ass_id):
    import os
    if os.path.isdir(str(ass_id)):
        return
    else:
        os.mkdir(str(ass_id))


def nameFile(sub):
    thefile = sub.attachments[-1]
    fname = thefile.__str__().replace(' ', '_')
    return f"{sub.assignment_id}/u{sub.user_id}_{fname}"


def download_submission(sub, suffix=None):

    if len(sub.attachments) > 0:
        mkdir(sub.assignment_id)
        thefile = sub.attachments[-1]
        downname = nameFile(sub)
        if suffix:
            if downname.endswith(suffix):
                thefile.download(downname)
        else:
            thefile.download(downname)


def cleanup(ass):
    import shutil
    shutil.rmtree(str(ass.id))


def get_submissions(ass):

    subs = ass.get_submissions()

    ungraded = [sub for sub in subs if len(sub.attachments) > 0 and
                (sub.grade == "0" or sub.grade is None)]
    for sub in tqdm(ungraded, desc=f"Downloading {ass.name}", ascii=True):
        download_submission(sub)

    return ungraded


def update_grade(sub, newgrade):
    sub.edit(submission={'posted_grade': str(newgrade)})


if __name__ == '__main__':
    args = options()
    choose_options(args)
