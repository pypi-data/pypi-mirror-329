from typing import List, Optional, Dict, Union
import requests
import altair as alt
import pandas as pd
import statistics

class Course:
    """A class to represent a course."""

    def __init__(self, course_code: str, course_id: int, token: str):
        """
        Initialize a Course instance.

        Parameters
        ----------
        course_code : str
            The code of the course (e.g., 'MATH101').
        course_id : int
            The unique identifier for the course.
        token : str
            Authentication token for the course.
        """
        self.course_code: str = course_code
        self.course_id: int = course_id
        self.students: List['Student'] = []
        self.assessments: List['Assessment'] = []
        self.token: str = token

    def fetch_students(self, global_students: Optional[Dict[int, 'Student']] = None) -> None:
        """Fetch all students in the course and populate the `students` list.

        Parameters
        ----------
        global_students : dict, optional
            A dictionary to map global student instances for reuse.
        """
        url = f"https://us.prairielearn.com/pl/api/v1/course_instances/{self.course_id}/gradebook"
        headers = {"Private-Token": self.token}
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            gradebook_data = response.json()

            for student in gradebook_data:

                student_id = student["user_id"]
                name = student["user_name"]
                email = student["user_uid"]

                # Create or retrieve the student instance
                if global_students is not None:
                    if student_id not in global_students:
                        student_instance = Student(student_id, name, email, self.token)
                        global_students[student_id] = student_instance
                    else:
                        student_instance = global_students[student_id]
                else:
                    student_instance = Student(student_id, name, email, self.token)

                # Add course to the student and append to the course's student list
                student_instance.add_course(self)
                self.students.append(student_instance)

            # Print the number of students fetched
            print(f"\nFetched {len(self.students)} students for course code {self.course_code}.")
        else:
            raise ValueError(f"Failed to fetch students. Status Code: {response.status_code}")

    def fetch_assessments(self, global_assessments: Optional[Dict[int, 'Assessment']] = None) -> None:
        """Fetch all assessments in the course and populate the `assessments` list.

        Parameters
        ----------
        global_assessments : dict, optional
            A dictionary to map global assessment instances for reuse.
        """
        url = f"https://us.prairielearn.com/pl/api/v1/course_instances/{self.course_id}/assessments"
        headers = {"Private-Token": self.token}
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            assessments_data = response.json()

            for assessment in assessments_data:

                assessment_id = assessment["assessment_id"]
                assessment_name = assessment["assessment_name"]
                assessment_label = assessment["assessment_label"]
                assessment_set_name = assessment["assessment_set_name"]
                assessment_set_heading = assessment["assessment_set_heading"]

                # Create or retrieve the assessment instance
                if global_assessments is not None:
                    if assessment_id not in global_assessments:
                        global_assessments[assessment_id] = Assessment(
                            assessment_id, assessment_name, assessment_label, assessment_set_name, assessment_set_heading, self.course_id, self.token
                        )
                    assessment_instance = global_assessments[assessment_id]
                else:
                    assessment_instance = Assessment(
                        assessment_id, assessment_name, assessment_label, assessment_set_name, assessment_set_heading, self.course_id, self.token
                    )

                # Append to the course's assessments list
                self.assessments.append(assessment_instance)

            # Print each assessment name on a new line
            print("Fetched assessments:")
            for assessment in self.assessments:
                print(f"- {assessment.name} (Label: {assessment.label})")
        else:
            raise ValueError(f"Failed to fetch assessments. Status Code: {response.status_code}")

    def show_student_list(self) -> None:
        """Show the list of students enrolled in the course."""
        if not self.students:
            self.fetch_students()
            
        print(f"\nThere are {len(self.students)} students in Course {self.course_code}:")

        for student in self.students:
            print(f"User ID: {student.user_id}, User Name: {student.user_name}, User UID: {student.user_uid}")

    def get_assessment_summary_statistics(self) -> None:
        """Compute and print summary statistics for each assessment in the course."""
        if not self.assessments:
            self.fetch_assessments()

        print("\nAssessment Summary Statistics:")
        for assessment in self.assessments:
            # Fetch submissions for the assessment
            assessment.fetch_submissions()

            # Get summary statistics using the Assessment class method
            stats = assessment.get_summary_statistics()

            if stats == None:
                print(f"\nNo submissions for Assessment: {assessment.name} (Label: {assessment.label})")
                continue
            
            print(f"\nAssessment: {assessment.name} (Label: {assessment.label})")
            print(f"  - Number of submissions: {stats['num_submissions']}")
            print(f"  - Mean score: {stats['mean_score']:.2f}%" if stats['mean_score'] is not None else "  - Mean score: N/A")
            print(f"  - Median score: {stats['median_score']:.2f}%" if stats['median_score'] is not None else "  - Median score: N/A")
            print(f"  - Max score: {stats['max_score']:.2f}%" if stats['max_score'] is not None else "  - Max score: N/A")
            print(f"  - Min score: {stats['min_score']:.2f}%" if stats['min_score'] is not None else "  - Min score: N/A")


    def plot_boxplot(self, assessment_label: Optional[List[str]] = None, assessment_name: Optional[List[str]] = None) -> None:
        """Plot boxplots for score distributions of all or specified assessments.

        Parameters
        ----------
        assessment_label : list of str, optional
            List of assessment labels to include in the plot.
        assessment_name : list of str, optional
            List of assessment names to include in the plot.
        """
        if not self.assessments:
            self.fetch_assessments()

        # Collect data for all or specified assessments
        data = []
        for assessment in self.assessments:
            # Include assessment if it matches either label or name filter
            if (
                not assessment_label and not assessment_name  # No filters provided
                or (assessment_label and assessment.label in assessment_label)  # Label filter matches
                or (assessment_name and assessment.name in assessment_name)  # Name filter matches
            ):
                # Fetch submissions for the assessment
                assessment.fetch_submissions()

                # Append the scores with assessment metadata
                data.extend([
                    {"assessment_name": f"{assessment.name} ({assessment.label})", "score": score}
                    for score in assessment.scores
                ])

        # Check if there's data to plot
        if not data:
            print("No data available to plot.")
            return

        # Convert to a DataFrame
        df = pd.DataFrame(data)

        # Create the Altair boxplot
        chart = (
            alt.Chart(df)
            .mark_boxplot()
            .encode(
                y=alt.Y("assessment_name:N", title="Assessments", sort=None),
                x=alt.X("score:Q", title="Score Percentage", scale=alt.Scale(domain=[0, 100])),
                color=alt.Color("assessment_name:N", legend=None),  # Optional for differentiation
                tooltip=["assessment_name", "score"],
            )
            .properties(
                title=f"Score Distribution Across Assessments in {self.course_code}",
                width=600,
                height=400,
            )
        )

        # Display the chart
        chart.display()
            

    def plot_histogram(self, assessment_label: Optional[List[str]] = None, assessment_name: Optional[List[str]] = None, bins: int = 20) -> None:
        """Plot a layered histogram for score distributions of all or specified assessments.

        Parameters
        ----------
        assessment_label : list of str, optional
            List of assessment labels to include in the plot.
        assessment_name : list of str, optional
            List of assessment names to include in the plot.
        bins : int, optional
            Number of bins for the histogram, default is 20.
        """
        if not self.assessments:
            self.fetch_assessments()

        # Collect data for all assessments
        data = []
        for assessment in self.assessments:
            # Include assessment if it matches either label or name filter
            if (
                not assessment_label and not assessment_name  # No filters provided
                or (assessment_label and assessment.label in assessment_label)  # Label filter matches
                or (assessment_name and assessment.name in assessment_name)  # Name filter matches
            ):

                assessment.fetch_submissions()

                # Append the scores with assessment metadata
                data.extend([
                    {"assessment_name": f"{assessment.name} ({assessment.label})", "score": score}
                    for score in assessment.scores
                ])

        # Check if there's data to plot
        if not data:
            print("No data available to plot.")
            return

        # Convert to a DataFrame
        df = pd.DataFrame(data)

        # Create the density curve
        density_chart = (
            alt.Chart(df)
            .transform_density(
                density="score",
                groupby=["assessment_name"],
                as_=["score", "density"]
            )
            .mark_area(opacity=0.5)
            .encode(
                x=alt.X("score:Q", title="Score Percentage"),
                y=alt.Y("density:Q", title="Density", stack=None),
                color=alt.Color("assessment_name:N", title="Assessments"),
            )
            .properties(
                title=f"Density Curve of Scores in {self.course_code}",
                width=600,
                height=400,
            )
        )

        # Display the chart
        density_chart.display()

class Assessment:
    """A class to represent an assessment in a course."""

    def __init__(self, assessment_id: int, name: str, label: str, set_name: str, set_heading: str, course_id: int, token: str):
        """
        Initialize an Assessment instance.

        Parameters
        ----------
        assessment_id : int
            The unique identifier for the assessment.
        name : str
            The name of the assessment.
        label : str
            A unique label for the assessment.
        set_name : str
            The set name for the asssessment.
        set_heading : str
            The set heading for the assessment.
        course_id : int
            The unique identifier for the course this assessment belongs to.
        token : str
            Authentication token for accessing course data.
        """
        self.assessment_id: int = assessment_id
        self.name: str = name
        self.label: str = label
        self.set_name: str = set_name
        self.set_heading: str = set_heading
        self.course_id: int = course_id
        self.token: str = token
        self.submissions: List[Dict] = []
        self.grouped_questions: Dict = {}

    def fetch_submissions(self) -> None:
        """Fetch all submissions for this assessment and populate the `scores` list.

        Raises
        ------
        ValueError
            If the API request fails.
        """
        url = f"https://us.prairielearn.com/pl/api/v1/course_instances/{self.course_id}/assessments/{self.assessment_id}/assessment_instances"
        headers = {"Private-Token": self.token}
        response = requests.get(url, headers=headers)

        submissions_list = []

        if response.status_code == 200:
            submissions = response.json()

            for submission in submissions:
                submissions_list.append({
                    'points': submission['points'],
                    'max_points': submission['max_points'],
                    'score_perc': submission['score_perc'],
                    'user_id': submission['user_id'],
                    'group_id': submission['group_id'],
                    'group_name': submission['group_name'],
                    'group_uids': submission['group_uids'],
                    'user_name': submission['user_name'],
                    'user_role': submission['user_role'],
                    'start_date': submission['start_date'],
                    'modified_at': submission['modified_at'],
                    'highest_score': submission['highest_score'],
                    'duration_seconds': submission['duration_seconds'],
                    'assessment_instance_id': submission['assessment_instance_id'],
                    'assessment_instance_number': submission['assessment_instance_number'],

                })

            print(f"Successfully fetched submissions for assessment '{self.name}' (ID: {self.assessment_id}).")
        else:
            raise ValueError(f"Failed to fetch submissions for assessment {self.name}. Status Code: {response.status_code}")

        self.submissions = submissions_list
        return submissions_list


    def fetch_submission_questions(self) -> List[Dict]:
        """
        Loops through each submission (assessment instance) and fetches the associated
        instance questions. Returns a flat list of all question features (with the submission metadata added).
        """
        # If there are no submissions fetched yet, fetch them first.
        if not self.submissions:
            self.fetch_submissions()

        all_question_features = []
        headers = {"Private-Token": self.token}

        for submission in self.submissions:
            assessment_instance_id = submission.get("assessment_instance_id")
            if not assessment_instance_id:
                print("Submission missing assessment instance ID")
                continue

            url = f"https://us.prairielearn.com/pl/api/v1/course_instances/{self.course_id}/assessment_instances/{assessment_instance_id}/instance_questions"
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                questions = response.json()
                # Add submission metadata to each question
                for question in questions:
                    question["assessment_instance_id"] = assessment_instance_id
                    question["user_id"] = submission.get("user_id")
                    question["user_name"] = submission.get("user_name")
                all_question_features.extend(questions)
            else:
                print(f"Error fetching questions for submission {assessment_instance_id}: {response.status_code}")
                print(response.text)

        return all_question_features

    def group_submission_questions(self) -> Dict:
        """
        Groups questions from all submissions by question_id. Each group contains the question features along with
        the associated assessment_instance_id, user_id, and user_name.

        Returns
        -------
        dict
            A dictionary where each key is a question_id and the value is a list of question entries.
        """
        # Fetch questions if needed
        all_questions = self.fetch_submission_questions()

        grouped = {}
        for question in all_questions:
            qid = question.get("question_id")
            if not qid:
                print(f"Question from submission {question.get('assessment_instance_id')} missing question_id, skipping.")
                continue

            if qid not in grouped:
                grouped[qid] = []
            grouped[qid].append(question)

        # Save grouped questions as an attribute for easy access later
        self.grouped_questions = grouped
        return grouped

    # def get_summary_statistics(self) -> Dict[str, float]:
    #     """Compute and return summary statistics for the scores.

    #     Returns
    #     -------
    #     dict
    #         A dictionary containing summary statistics:
    #         - num_submissions : int
    #             Number of submissions.
    #         - mean_score : float
    #             Average score percentage.
    #         - median_score : float
    #             Median score percentage.
    #         - max_score : float
    #             Maximum score percentage.
    #         - min_score : float
    #             Minimum score percentage.
        
    #     Raises
    #     ------
    #     ValueError
    #         If there are no scores available.
    #     """
    #     if not self.scores:
    #         self.fetch_submissions()

    #     if not self.scores:
    #         return None

    #     return {
    #         "num_submissions": len(self.scores),
    #         "mean_score": sum(self.scores) / len(self.scores),
    #         "median_score": statistics.median(self.scores),
    #         "max_score": max(self.scores),
    #         "min_score": min(self.scores),
    #     }

    # def plot_score_histogram(self) -> None:
    #     """Plot a histogram of the score percentages using Altair."""
    #     if not self.scores:
    #         self.fetch_submissions()

    #     # Create a DataFrame from the scores
    #     df = pd.DataFrame({"scores": self.scores})

    #     # Create the Altair histogram
    #     histogram = (
    #         alt.Chart(df)
    #         .mark_bar()
    #         .encode(
    #             x=alt.X("scores:Q", bin=alt.Bin(maxbins=10), title="Score Percentage"),
    #             y=alt.Y("count():Q", title="Frequency"),
    #             tooltip=[
    #                 alt.Tooltip("scores:Q", title="Score Range"),
    #                 alt.Tooltip("count():Q", title="Frequency")
    #             ]
    #         )
    #         .properties(
    #             title=f"Score Distribution for {self.name} (Label: {self.label})",
    #             width=600,
    #             height=400
    #         )
    #     )

    #     # Display the histogram
    #     histogram.display()


class Student:
    """A class to represent a student."""
    
    def __init__(self, user_id: int, user_name: str, user_uid: str, token: str):
        """
        Initialize a Student instance.

        Parameters
        ----------
        user_id : int
            The unique identifier for the student.
        user_name : str
            The name of the student.
        user_uid : str
            The UID (email or unique identifier) of the student.
        token : str
            Authentication token for accessing data.
        """
        self.user_id: int = user_id
        self.user_name: str = user_name
        self.user_uid: str = user_uid
        self.token: str = token
        self.courses: List['Course'] = []
        self.grades: List[Dict[str, Union[str, int, float]]] = []

    def add_course(self, course: 'Course') -> None:
        """Add a course to the student's list of courses.

        Parameters
        ----------
        course : Course
            The course to add to the student's list.
        """
        if course not in self.courses:
            self.courses.append(course)

    def list_courses(self) -> None:
        """Print the student's name and the courses they are enrolled in."""
        print(f"Student: {self.user_name}")
        if self.courses:
            print("Enrolled in the following courses:")
            for course in self.courses:
                print(f"- Course ID: {course.course_id}")
        else:
            print("Not enrolled in any courses.")

    def fetch_all_grades(self) -> List[Dict[str, Union[str, int, float]]]:
        """Fetch all grades for the student across their courses.

        Returns
        -------
        list of dict
            A list of dictionaries containing grades for each assessment.

        Raises
        ------
        ValueError
            If the gradebook cannot be fetched for any course.
        """
        grades = []
        for course in self.courses:
            url = f"https://us.prairielearn.com/pl/api/v1/course_instances/{course.course_id}/gradebook"
            headers = {"Private-Token": self.token}
            response = requests.get(url, headers=headers)

            if response.status_code == 200:
                gradebook_data = response.json()
                student_data = next((student for student in gradebook_data if student["user_id"] == self.user_id), None)

                if student_data:
                    for assessment in student_data["assessments"]:

                        grades.append({
                            "course_code": course.course_code,
                            "course_id": course.course_id,
                            "points": assessment["points"],
                            "max_points": assessment["max_points"],
                            "score_perc": assessment["score_perc"],
                            "start_date": assessment["start_date"],
                            "duration_seconds": assessment["duration_seconds"],
                            "assessment_id": assessment["assessment_id"],
                            "assessment_name": assessment["assessment_name"],
                            "assessment_label": assessment["assessment_label"],
                        })

            else:
                raise ValueError(f"Failed to fetch gradebook for course {course.course_id}. Status Code: {response.status_code}")

        print(f"Successfully fetched all grades for student {self.user_name} (ID: {self.user_id})")
        self.grades = grades
        return grades

    def plot_grades(self, course_code: Optional[Union[str, List[str]]] = None, assessment_label: Optional[Union[str, List[str]]] = None) -> None:
        """Plot the grades of the student using Altair. Optionally filter by course or assessment.

        Parameters
        ----------
        course_code : str or list of str, optional
            The course code(s) to filter grades by.
        assessment_label : str or list of str, optional
            The assessment label(s) to filter grades by.

        Raises
        ------
        ValueError
            If no grades are available for the specified filters.
        """
        if not self.grades:
            self.fetch_all_grades()

        if isinstance(course_code, str):
            course_code = [course_code]
        if isinstance(assessment_label, str):
            assessment_label = [assessment_label]

        grades_to_plot = [
            grade for grade in self.grades
            if (course_code is None or grade["course_code"] in course_code) and
            (assessment_label is None or grade["assessment_label"] in assessment_label)
        ]

        if not grades_to_plot:
            filters = []
            if course_code:
                filters.append(f"course(s): {', '.join(course_code)}")
            if assessment_label:
                filters.append(f"assessment label(s): {', '.join(assessment_label)}")
            raise ValueError(f"No grades found for {', '.join(filters)}.")

        df = pd.DataFrame(grades_to_plot)
        df["score_perc"] = df["score_perc"].fillna(0)
        df["true_assessment_name"] = (
            df["course_code"] + " - " + df["assessment_name"] + " (" + df["assessment_label"] + ")"
        )

        bars = (
            alt.Chart(df)
            .mark_bar()
            .encode(
                x=alt.X("score_perc:Q", title="Score Percentage", scale=alt.Scale(domain=[0, 100])),
                y=alt.Y("true_assessment_name:N", title="Assessments", sort=None),
                color=alt.Color("course_code:N", title="Course Code"),
                tooltip=["course_code", "assessment_name", "assessment_label", "score_perc"],
            )
            .properties(
                width=600,
                height=400,
            )
        )

        annotations = (
            alt.Chart(df)
            .mark_text(dx=15, fontSize=10, fontWeight="bold", color="black")
            .encode(
                y=alt.Y("true_assessment_name:N", sort=None),
                x=alt.X("score_perc:Q"),
                text=alt.Text("score_perc:Q", format=".1f"),
            )
        )

        chart = (bars + annotations).properties(
            title=f"Grades for {self.user_name}" + (f" in {', '.join(course_code)}" if course_code else "")
        )

        return chart
