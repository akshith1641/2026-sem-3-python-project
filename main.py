import json
import os

COMPLAINTS_FILE = "complaints.json"
MANAGER_USERNAME = "manager"
MANAGER_PASSWORD = "manager123"
STARTING_ID_NUMBER = 101


def load_complaints():
    if not os.path.exists(COMPLAINTS_FILE):
        return []

    try:
        file = open(COMPLAINTS_FILE, "r")
        content = file.read()
        file.close()

        if content.strip() == "":
            return []

        complaints = json.loads(content)
        return complaints

    except Exception as e:
        # file reading failed, so starting fresh only
        print("Warning: Could not read complaints file. Starting fresh.")
        print("Error details:", e)
        return []


def save_complaints(complaints):
    try:
        file = open(COMPLAINTS_FILE, "w")
        json.dump(complaints, file, indent=4)
        file.close()
    except Exception as e:
        print("Error: Could not save complaints.")
        print("Error details:", e)


def generate_complaint_id(complaints):
    if len(complaints) == 0:
        return "CP" + str(STARTING_ID_NUMBER)

    highest_number = STARTING_ID_NUMBER - 1

    for complaint in complaints:
        id_text = complaint["complaint_id"]
        number_part = id_text[2:]  # removing "CP" from front to get number

        try:
            number = int(number_part)
            if number > highest_number:
                highest_number = number
        except:
            pass

    new_number = highest_number + 1
    return "CP" + str(new_number)


def display_complaint(complaint):
    print("--------------------------------------------")
    print("  Complaint ID  :", complaint["complaint_id"])
    print("  Student Name  :", complaint["student_name"])
    print("  Hostel/Block  :", complaint["hostel"])
    print("  Room Number   :", complaint["room_number"])
    print("  Category      :", complaint["category"])
    print("  Description   :", complaint["description"])
    print("  Status        :", complaint["status"])
    print("--------------------------------------------")


def get_category():
    print("\n  Select Complaint Category:")
    print("  1. Wi-Fi")
    print("  2. Water Supply")
    print("  3. Electricity")
    print("  4. Cleaning")
    print("  5. Maintenance")
    print("  6. Other")

    while True:
        choice = input("\n  Enter your choice (1-6): ").strip()

        if choice == "1":
            return "Wi-Fi"
        elif choice == "2":
            return "Water Supply"
        elif choice == "3":
            return "Electricity"
        elif choice == "4":
            return "Cleaning"
        elif choice == "5":
            return "Maintenance"
        elif choice == "6":
            return "Other"
        else:
            print("  Invalid choice. Please enter a number from 1 to 6.")


def submit_complaint(complaints):
    print("\n====================================")
    print("  Submit a Complaint")
    print("====================================")

    while True:
        student_name = input("\n  Enter your name: ").strip()
        if student_name == "":
            print("  Name cannot be empty. Please enter your name.")
        else:
            break

    while True:
        hostel = input("  Enter your hostel name or block: ").strip()
        if hostel == "":
            print("  Hostel name cannot be empty. Please enter your hostel name.")
        else:
            break

    room_number = input("  Enter your room number (press Enter to skip): ").strip()
    if room_number == "":
        room_number = "Not provided"

    category = get_category()

    while True:
        print("\n  Describe your complaint in detail:")
        description = input("  > ").strip()
        if description == "":
            print("  Description cannot be empty. Please describe your complaint.")
        else:
            break

    new_id = generate_complaint_id(complaints)

    # making the complaint as dictionary and saving
    new_complaint = {
        "complaint_id": new_id,
        "student_name": student_name,
        "hostel": hostel,
        "room_number": room_number,
        "category": category,
        "description": description,
        "status": "Pending"
    }

    complaints.append(new_complaint)
    save_complaints(complaints)

    print("\n  Complaint submitted successfully!")
    print("  Your Complaint ID is:", new_id)
    print("  Please save this ID to check your complaint status later.")
    print("  Status: Pending")


def view_my_complaints(complaints):
    print("\n====================================")
    print("  View My Complaints")
    print("====================================")

    student_name = input("\n  Enter your name to search: ").strip()

    if student_name == "":
        print("  Name cannot be empty.")
        return

    # using lower() so name matching not case sensitive
    found_complaints = []
    for complaint in complaints:
        if complaint["student_name"].lower() == student_name.lower():
            found_complaints.append(complaint)

    if len(found_complaints) == 0:
        print("\n  No complaints found for the name:", student_name)
        print("  Please check your name and try again.")
    else:
        print("\n  Found", len(found_complaints), "complaint(s) for:", student_name)
        for complaint in found_complaints:
            display_complaint(complaint)


def manager_login():
    print("\n====================================")
    print("  Manager Login")
    print("====================================")

    username = input("\n  Username: ").strip()
    password = input("  Password: ").strip()

    if username == MANAGER_USERNAME and password == MANAGER_PASSWORD:
        print("\n  Login successful! Welcome, Manager.")
        return True
    else:
        print("\n  Incorrect username or password. Access denied.")
        return False


def view_all_complaints(complaints):
    print("\n====================================")
    print("  All Complaints")
    print("====================================")

    if len(complaints) == 0:
        print("\n  No complaints have been submitted yet.")
        return

    print("\n  Total complaints:", len(complaints))

    for complaint in complaints:
        display_complaint(complaint)


def update_complaint_status(complaints):
    print("\n====================================")
    print("  Update Complaint Status")
    print("====================================")

    if len(complaints) == 0:
        print("\n  No complaints available to update.")
        return

    complaint_id = input("\n  Enter the Complaint ID to update (e.g., CP101): ").strip().upper()

    found_complaint = None
    found_index = -1

    for i in range(len(complaints)):
        if complaints[i]["complaint_id"] == complaint_id:
            found_complaint = complaints[i]
            found_index = i
            break

    if found_complaint is None:
        print("\n  Complaint ID", complaint_id, "not found.")
        print("  Please check the ID and try again.")
        return

    print("\n  Complaint found:")
    display_complaint(found_complaint)

    print("\n  Select new status:")
    print("  1. Pending")
    print("  2. In Progress")
    print("  3. Resolved")

    while True:
        choice = input("\n  Enter your choice (1-3): ").strip()

        if choice == "1":
            new_status = "Pending"
            break
        elif choice == "2":
            new_status = "In Progress"
            break
        elif choice == "3":
            new_status = "Resolved"
            break
        else:
            print("  Invalid choice. Please enter 1, 2, or 3.")

    # updating status and saving to file
    complaints[found_index]["status"] = new_status
    save_complaints(complaints)

    print("\n  Status updated successfully!")
    print("  Complaint ID:", complaint_id)
    print("  New Status  :", new_status)


def view_complaint_summary(complaints):
    print("\n====================================")
    print("  Complaint Summary")
    print("====================================")

    if len(complaints) == 0:
        print("\n  No complaints have been submitted yet.")
        return

    total = len(complaints)
    pending_count = 0
    in_progress_count = 0
    resolved_count = 0

    for complaint in complaints:
        if complaint["status"] == "Pending":
            pending_count = pending_count + 1
        elif complaint["status"] == "In Progress":
            in_progress_count = in_progress_count + 1
        elif complaint["status"] == "Resolved":
            resolved_count = resolved_count + 1

    print("\n  Total Complaints    :", total)
    print("  Pending             :", pending_count)
    print("  In Progress         :", in_progress_count)
    print("  Resolved            :", resolved_count)
    print("")


def manager_menu(complaints):
    while True:
        print("\n====================================")
        print("  CampusPulse Manager")
        print("====================================")
        print("  1. View All Complaints")
        print("  2. Update Complaint Status")
        print("  3. View Complaint Summary")
        print("  4. Logout")
        print("====================================")

        choice = input("\n  Enter your choice: ").strip()

        if choice == "1":
            view_all_complaints(complaints)

        elif choice == "2":
            update_complaint_status(complaints)

        elif choice == "3":
            view_complaint_summary(complaints)

        elif choice == "4":
            print("\n  Logged out. Returning to main menu.")
            break

        else:
            print("\n  Invalid choice. Please enter 1, 2, 3, or 4.")


def main():
    # loading complaints from file when program starts
    complaints = load_complaints()

    print("\n====================================")
    print("  Welcome to CampusPulse")
    print("  IIIT Kottayam")
    print("  Hostel Issue Management System")
    print("====================================")

    while True:
        print("\n====================================")
        print("  MAIN MENU")
        print("====================================")
        print("  1. Submit a Complaint")
        print("  2. View My Complaints")
        print("  3. Manager Login")
        print("  4. Exit")
        print("====================================")

        choice = input("\n  Enter your choice: ").strip()

        if choice == "1":
            submit_complaint(complaints)

        elif choice == "2":
            view_my_complaints(complaints)

        elif choice == "3":
            login_successful = manager_login()
            if login_successful:
                manager_menu(complaints)

        elif choice == "4":
            print("\n====================================")
            print("  Thank you for using CampusPulse!")
            print("  Goodbye!")
            print("====================================\n")
            break

        else:
            print("\n  Invalid choice. Please enter 1, 2, 3, or 4.")


if __name__ == "__main__":
    main()
