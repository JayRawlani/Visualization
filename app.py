from flask import Flask, render_template, request, redirect, url_for
import os
from os.path import join, dirname, realpath
import random 
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

app = Flask(__name__)

UPLOAD_FOLDER = 'static/files'
app.config['UPLOAD_FOLDER'] =  UPLOAD_FOLDER

@app.route('/')
def index():
    return render_template('index.html')

@app.route("/", methods=['POST'])
def uploadFiles():
        # get the uploaded file
        uploaded_file = request.files['file']
        if uploaded_file.filename != '':
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], uploaded_file.filename)
            # set the file path
            uploaded_file.save(file_path)
            print(uploaded_file.filename)
            # save the file
        
        depart = ['Comp', 'IT','ETC','Chem','Civil','Mech']
        df = pd.read_csv(file_path)
        df.head(30)

        df.shape

        df.info

        #Name of student with highest percentage around all the branches
        print(df['Name'][df['Percentage'] == df['Percentage'].max()])

        #name of student with lowest percentage around all the branches
        print(df['Name'][df['Percentage'] == df['Percentage'].min()])

        #Group By
        gb = df.groupby('Department')
        #Getting the forst element from each and every group
        gb.first()
        #getting dets about each IT group
        IT = gb.get_group('IT')
        print(IT)
        #print(IT['Name'])
        #Name of student with min marks in IT department
        min_IT = IT['Name'][IT['Percentage'] == IT['Percentage'].min()] 
        print(min_IT)
        #Name of the student with max marks in IT department
        max_IT = IT['Name'][IT['Percentage'] == IT['Percentage'].max()] 
        print(max_IT)
        #Average Percentage of IT department
        print(IT['Percentage'].mean())

        #Taking Input from the user to generalise the details reg min and max marks from any departments
        dept =  input("Enter the name of the department:- ")
        print(dept)
        #Extracting details of the particular depart for further analysis
        dept_gb = gb.get_group(dept)
        print("Details of the department\n", dept_gb)

        #Min marks from the selected department 
        min_marks_dept = dept_gb['Name'][dept_gb['Percentage'] == dept_gb['Percentage'].min()] 
        print("Student with Min marks in the Depart ",min_marks_dept )
        #Max marks from the selected department
        max_marks_dept = dept_gb['Name'][dept_gb['Percentage'] == dept_gb['Percentage'].max()] 
        print("Student with Max marks in the Depart",max_marks_dept)
        #Average marks form the selected department
        print(dept_gb['Percentage'].mean())

        ##To Get marks from the selected Subjects
        #Extracting the name of columns from the dataset
        sub = list(dept_gb.columns.values[2:7])
        print("Subject Names" , sub)

        sub_name =  input("Enter the name of the Subject:- ")
        x =  int(input("Press 1. for Specific Student Subject result \n Press 2 for Department Subject Result:- "))

        if(x==1):
            stu_name = input("Enter the name of the student:- ")
            y = np.where(dept_gb["Name"] == stu_name)
            print(y)
            print("Details of teh student are\n",dept_gb.iloc[y[0][0]])
        else:
            print(dept_gb[sub_name])


        #Extracting the Data for a prticular student in the Department

        stu_name = input("Enter the name of the student:- ")
        z = np.where(dept_gb["Name"] == stu_name)
        print("Details of teh student are\n",dept_gb.iloc[z[0][0]])

        y = np.where(dept_gb["Name"] == stu_name)
        print(y[0][0])

        """Model Testing - """

        df = pd.read_csv("Final.csv")

        data = pd.read_csv(file_path)

        Columns  = list(data.columns.values)
        #print(Columns)

        Columns = ['Percentage']

        count = [0] * df.shape[0]
        #print(count)

        arr = []

        for i in df:
            for j in df[i]:
                a1 = 0
                if j in Columns:
                    a1 = a1+1
                if(a1==df.shape[0]):
                    a1 = 0
                    arr.append(a1)

        for i in range(len(arr)):
            count[i%9] = count[i%9] + arr[i]

        #print(count)
        Quest = []
        if (len(Columns)==1):
            for i in range(len(count)):
                if(count[i]>=1):
                    Quest.append(df.at[i,'QUESTIONS'])
        else:
            for i in range(len(count)):
                if(count[i]>1):
                    Quest.append(df.at[i,'QUESTIONS'])
        #print(Quest)
        """#Visualisation

        """



        df = pd.read_csv(file_path)

        sns.set_theme(style="whitegrid")
        a = depart
        b = []
        gb = df.groupby('Department')

        for i in range(len(depart)):
            dept =  depart[i]
            dept_gb = gb.get_group(dept)
            b.append(round(dept_gb['Percentage'].mean(),2))

        print("Mean Percentage of Students in each Deptartment\n",a,b)

        ax = sns.barplot(x=a, y=b)
        ax.set_title('Average percentage of each department')

        #subject wise average marks
        sub = ['M1','EGR', 'CHEM', 'Python','EEE']
        sub_mean = []
        for i in range(len(sub)):
            sub_mean.append(round(df[sub[i]].mean(),2))

        print("Mean Percentage of Students in each Subject\n",sub,sub_mean)

        ax = sns.barplot(x=sub, y=sub_mean)
        ax.set_title('Average marks of each subject')

        #Count of student above a particular marks in each department

        a = depart
        b = []
        gb = df.groupby('Department')

        for i in range(len(depart)):
            dept =  depart[i]
            dept_gb = gb.get_group(dept)
            b.append(dept_gb[(dept_gb['M1']>90)]['Name'].count())
        

        print(a,b)

        ax = sns.barplot(x=a, y=b)
        ax.set_title('M1 marks greater in 90 in each department')

        #Count of student above a particular marks in each department

        a = depart
        b = []
        gb = df.groupby('Department')
        for i in range(len(depart)):
            dept =  depart[i]
            dept_gb = gb.get_group(dept)
            for j in range(len(sub)):
                b.append(dept_gb[(dept_gb[str(sub[j])]>90)]['Name'].count())
            print(dept, sub,b)
            ax = sns.color_palette('bright')[0:5]
            plt.pie(b, labels = sub, colors = ax , autopct='%.0f%%')
            plt.title(('Percentage of student in ' + dept + ' who scored above 90 in particular subject'))
            plt.show()
            b = []

        return redirect(url_for('index'))


if __name__ == "__main__":
    app.run(debug=True)

