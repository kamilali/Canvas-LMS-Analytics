'''
	Canvas Course Analytics Script

'''
import requests
import json

# This function checks if the passed in value is a number
def is_number(value):
	try:
		float(value)
		return True
	except ValueError:
		return False

# Class for all courses. Contains important information such as:
# 1) Course Name
# 2) Course Number
# 3) Credit Hours
# 4) Undergraduate or Graduate Course?
# 5) Number of Users Enrolled In Course

class Course(object):

	def __init__(self, course):
		self.course = course
		self.course_num = course[(course.index(" ") + 1):]
		self.credit_hours = int(course[(course.index(" ") + 1):(course.index(" ") + 2)])
		self.grad_standing = self.is_grad_standing()
		self.num_students = self.get_total_enrollment()

	# This method sets the init variable num_students (how many total students are enrolled in the course)
	def get_total_enrollment(self):

		# Get a list of students by course id

		# temporary course id for testing 
		course_id = ########

		# authentication token for testing
		auth_token = "<your authentication token>"

		# URL call to API for data
		query_url = "https://<your canvas instance>.instructure.com/api/v1/courses/" + str(course_id) + "/students"
		
		# Must pass the auth_token through header (also could do through string, however, not safe)
		headers = {"Authorization": "Bearer " + auth_token}

		# Extract students json object
		students = requests.get(query_url, headers=headers).json()

		# Get number of enrolled students and return value
		return len(students)

	# This method sets the init variable grad_standing (is the course a graduate course)
	def is_grad_standing(self):

		str_len = len(self.course_num)
		last_index = str_len - 1

		tail = self.course_num[last_index:]
		grad_standing = False

		str_len = len(self.course_num)
		last_index = str_len - 1

		# Check if the tail of the course name is a number or a letter (this
		# will determine how we extract the last two digits of the course name
		# which will determine whether it is a grad course or undergrad course
		# as per the specs of the university)
		if is_number(tail):
			grad_standing = True if int(self.course_num[1:]) >= 80 else False
		else:
			grad_standing = True if int(self.course_num[1:last_index]) >= 80 else False

		return grad_standing

	# This method prints course information 
	def print_course_info(self):

		course_level = "Graduate" if self.grad_standing else "Undergraduate"

		print("Course Information for " + self.course + ":")
		print("Course Number: " + self.course_num + "\nCredit Hours: " + str(self.credit_hours) + "\nCourse Level: " + course_level + "\nNumber of Enrolled Students:" + str(self.num_students) + "\n")


if __name__ == '__main__':

	# Test Cases
	course = Course("ACC 321L")
	course1 = Course("ACC 380")
	course.print_course_info()
	course1.print_course_info()