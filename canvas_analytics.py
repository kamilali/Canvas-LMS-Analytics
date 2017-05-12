'''
	Canvas Course Analytics Script

'''
import requests
import json


# authentication token for testing
auth_token = "<Your authentication token>"

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

	def __init__(self, course, course_id):
		self.course = course

		# credit hours from sis id
		first_index = course_id.index("_") + 1
		self.credit_hours = int(course_id[first_index, first_index + 1])
		self.course_num = course_id[first_index, course_id.index("_", first_index)]
		self.grad_standing = self.is_grad_standing()
		self.num_students = self.get_total_enrollment(course_id)

	# This method sets the init variable num_students (how many total students are enrolled in the course)
	def get_total_enrollment(self, course_id):

		# Get a list of students by course id

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
			# In the case of a course that doesn't follow general guidelines
			# (i.e. training courses, etc), we will default it to undergrad
			if not is_number(self.course_num[1:]):
				return False

			# If the last two numbers do compose an int, then we check for grad standing
			grad_standing = True if int(self.course_num[1:]) >= 80 else False
		else:
			# In the case of a course that doesn't follow general guidelines
			# (i.e. training courses, etc), we will default it to undergrad
			if not is_number(self.course_num[1:]):
				return False

			# If the middle two numbers do compose an int, then we check for grad standing
			grad_standing = True if int(self.course_num[1:last_index]) >= 80 else False

		return grad_standing

	# This method prints course information 
	def print_course_info(self):

		course_level = "Graduate" if self.grad_standing else "Undergraduate"

		print("Course Information for " + self.course + ":")
		print("Course Number: " + self.course_num + "\nCredit Hours: " + str(self.credit_hours) + "\nCourse Level: " + course_level + "\nNumber of Enrolled Students:" + str(self.num_students) + "\n")


def get_all_courses(url, headers):

	courses = []

	# Since canvas limits number of elements we can get per page, we will use pagination to get all courses
	course_listing_response = requests.get(url, headers=headers)
	for course in course_listing_response.json():
		curr_course = {}
		curr_course['course_code'] = course['course_code']
		curr_course['course_id'] = course['id']
		courses.append(curr_course)

	#while course_listing_response
	while course_listing_response.links['current']['url'] != course_listing_response.links['last']['url']:

		# There are still more courses to extract, so we grab the next url and request for the next batch
		course_listing_response = requests.get(course_listing_response.links['next']['url'], headers=headers)

		for course in course_listing_response.json():
			curr_course = {}
			curr_course['course_code'] = course['course_code']
			curr_course['course_id'] = course['sis_course_id']
			courses.append(curr_course)

	return courses



if __name__ == '__main__':

	# Information we need to get list of all courses
	url = "https://<your canvas instance>.instructure.com/api/v1/accounts/<account id>/courses?enrollment_term_id=<enrollement term id>&per_page=100"
	headers = {"Authorization": "Bearer " + auth_token}

	# We get all the courses in our canvas instance
	courses = get_all_courses(url, headers)
	
	# Get info for each course
	for course in courses:
		curr_course = Course(course['course_code'], int(course['course_id']))
		curr_course.print_course_info()