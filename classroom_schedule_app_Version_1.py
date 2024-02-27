import streamlit as st
from datetime import datetime, timedelta

def generate_dates(class_info, start_date, end_date, sort_option):
    dates = []
    current_date = datetime.combine(start_date, datetime.min.time())

    while current_date <= datetime.combine(end_date, datetime.min.time()):
        for class_number, working_hours in class_info.items():
            for day, selected_hours in working_hours.items():
                # Skip days with no scheduled class
                if not selected_hours:
                    continue

                for selected_hour in selected_hours:
                    start_time, end_time = map(str.strip, selected_hour.split('-'))
                    start_hour, start_minute = map(int, start_time.split(':'))
                    end_hour, end_minute = map(int, end_time.split(':'))

                    # Calculate the day of the week based on the provided input
                    input_day_index = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday","Saturday"].index(day)
                    target_day_index = (input_day_index - current_date.weekday() + 7) % 7
                    target_date = current_date + timedelta(days=target_day_index)

                    start_datetime = datetime(target_date.year, target_date.month, target_date.day, start_hour, start_minute)
                    end_datetime = datetime(target_date.year, target_date.month, target_date.day, end_hour, end_minute)

                    date_str = f"{start_datetime.strftime('%Y-%m-%d')} : {start_datetime.strftime('%H:%M')} - {end_datetime.strftime('%H:%M')}"

                    # Check if the date is already added and within the end_date
                    if (class_number, day, date_str) not in dates and start_datetime.date() <= end_date:
                        dates.append((class_number, day, date_str))

        current_date += timedelta(days=1)

    # Sort dates based on the specified options
    if sort_option == "Date":
        dates.sort(key=lambda x: datetime.strptime(x[2].split(' : ')[0], "%Y-%m-%d") + timedelta(hours=int(x[2].split(' - ')[0].split(':')[-1])))
    elif sort_option == "Day":
        dates.sort(key=lambda x: (x[1], datetime.strptime(x[2].split(' : ')[0], "%Y-%m-%d") + timedelta(hours=int(x[2].split(' - ')[0].split(':')[-1]))))
    elif sort_option == "Class":
        dates.sort(key=lambda x: (x[0], datetime.strptime(x[2].split(' : ')[0], "%Y-%m-%d") + timedelta(hours=int(x[2].split(' - ')[0].split(':')[-1]))))

    return dates

def main():
    st.title("Class Schedule Viewer")

    # Get input for each class schedule
    class_info = {}
    st.header("Enter Class Information:")
    input_count = 0
    while True:
        class_number = st.text_input(f"Class Number {input_count+1} (enter the class Name)", key=f"class_number_{input_count}")
        if not class_number:
            break

        working_hours = {}
        s = {}
        Monday, Tuesday, Wednesday, Thursday, Friday,Saturday= st.columns(6)
        with Monday:
            selected_hours = st.multiselect(f"Monday :", ["08:00-09:00", "09:00-10:00", "10:00-11:00", "11:00-12:00", "14:00-15:00", "15:00-16:00", "16:00-17:00", "17:00-18:00"], key=f"hours_input_{class_number}_Monday")
            working_hours["Monday"] = selected_hours        
        with Tuesday:
            selected_hours = st.multiselect(f"Tuesday :", ["08:00-09:00", "09:00-10:00", "10:00-11:00", "11:00-12:00", "14:00-15:00", "15:00-16:00", "16:00-17:00", "17:00-18:00"], key=f"hours_input_{class_number}_Tuesday")
            working_hours["Tuesday"] = selected_hours 
        with Wednesday:
            selected_hours = st.multiselect(f"Wednesday :", ["08:00-09:00", "09:00-10:00", "10:00-11:00", "11:00-12:00", "14:00-15:00", "15:00-16:00", "16:00-17:00", "17:00-18:00"], key=f"hours_input_{class_number}_Wednesday")
            working_hours["Wednesday"] = selected_hours 
        with Thursday:
            selected_hours = st.multiselect(f"Thursday :", ["08:00-09:00", "09:00-10:00", "10:00-11:00", "11:00-12:00", "14:00-15:00", "15:00-16:00", "16:00-17:00", "17:00-18:00"], key=f"hours_input_{class_number}_Thursday")
            working_hours["Thursday"] = selected_hours 
        with Friday:
            selected_hours = st.multiselect(f"Friday :", ["08:00-09:00", "09:00-10:00", "10:00-11:00", "11:00-12:00", "14:00-15:00", "15:00-16:00", "16:00-17:00", "17:00-18:00"], key=f"hours_input_{class_number}_Friday")
            working_hours["Friday"] = selected_hours 
        with Saturday:
            selected_hours = st.multiselect(f"Saturday :", ["08:00-09:00", "09:00-10:00", "10:00-11:00", "11:00-12:00", "14:00-15:00", "15:00-16:00", "16:00-17:00", "17:00-18:00"], key=f"hours_input_{class_number}_Saturday")
            working_hours["Saturday"] = selected_hours 


       
           
           

        class_info[class_number] = working_hours
        input_count += 1

    # Display the input class information
    st.header("Class Information:")
    for class_number, working_hours in class_info.items():
        st.subheader(f"Class {class_number} Working Hours:")
        Monday, Tuesday, Wednesday, Thursday, Friday,Saturday= st.columns(6)
        with Monday:
            st.write(f"Monday :")
            st.write(f"{working_hours['Monday']}")
        with Tuesday:
            st.write(f"Tuesday :")
            st.write(f"{working_hours['Tuesday']}")
        with Wednesday:
            st.write(f"Wednesday :")
            st.write(f"{working_hours['Wednesday']}")
        with Thursday:
            st.write(f"Thursday :")
            st.write(f"{working_hours['Thursday']}")
        with Friday:
            st.write(f"Friday :")
            st.write(f"{working_hours['Friday']}")
        with Saturday:
            st.write(f"Saturday :")
            st.write(f"{working_hours['Saturday']}")


    # Get the starting and ending dates for schedule generation
    start,end = st.columns(2)
    with start:
        start_date = st.date_input("Starting Date", datetime.now().date())
    with end:
        end_date = st.date_input("Ending Date", datetime.now().date())

    # Choose the sorting options
    sort_option = st.radio("Sort Schedule By:", ("Date", "Day", "Class"),horizontal=True)

    if st.button("Generate Schedule"):
        # Generate dates based on the class schedules, starting/ending dates, and sorting options
        generated_dates = generate_dates(class_info, start_date, end_date, sort_option)
        st.header("Generated Dates Sorted:")

        # Create a table for the output
        table_data = []
        for class_number, day, time_range in generated_dates:
            table_data.append([class_number, day, time_range])

        # Display the table
        st.table(table_data)

if __name__ == "__main__":
    main()
