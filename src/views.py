from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required#decorator is used to restrict the access of the view to only authenticated users. If a user is not authenticated, they will be redirected to the login page specified in the login_url parameter.
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login,logout

# Create your views here.

@login_required(login_url='login')
def index(request):
    return render(request,'index.html')


@login_required(login_url='login')
def ckd_prediction(request):
    if request.method == "POST":

        data = request.POST

        # ------------------ GET USER INPUT ------------------
        age = float(data.get('Age'))
        bmi = float(data.get('BMI'))
        systolic_bp = float(data.get('Systolic_BP'))
        diastolic_bp = float(data.get('Diastolic_BP'))
        heart_rate = float(data.get('Heart_Rate'))
        sodium = float(data.get('Sodium'))
        potassium = float(data.get('Potassium'))
        hemoglobin = float(data.get('Hemoglobin'))
        gender = int(data.get('Gender'))
        diabetes = int(data.get('Diabetes'))
        hypertension = int(data.get('Hypertension'))
        smoking = int(data.get('Smoking_Status'))

        if 'buttonadd' in request.POST:

            import numpy as np
            import pandas as pd

            # ------------------ LOAD DATA ------------------
            train_path = "C:\\Users\\Windows 10\\Desktop\\karunadu_internship\\Project_01\\data\\Project_Dataset_2026\\Chronic Kidney Disease (CKD) Clinical Dataset\\Training_CKD_dataset.csv"
            test_path = "C:\\Users\\Windows 10\\Desktop\\karunadu_internship\\Project_01\\data\\Project_Dataset_2026\\Chronic Kidney Disease (CKD) Clinical Dataset\\Testing_CKD_dataset.csv"

            train_data = pd.read_csv(train_path)
            test_data = pd.read_csv(test_path)

            # ------------------ PREPROCESS ------------------
            def preprocess(data):
                data = data.copy()

                # Yes/No → 1/0
                data.replace({'Yes': 1, 'No': 0}, inplace=True)

                # Clean Target
                data['Target'] = data['Target'].astype(str).str.strip()
                data['Target'] = data['Target'].str.replace('–', '-', regex=True)

                # Mapping (4 classes)
                data['Target'] = data['Target'].map({
                    'Healthy Kidney': 0,
                    'Mild CKD (Stage 1-2)': 1,
                    'Moderate CKD (Stage 3)': 2,
                    'Severe CKD (Stage 4)': 3
                })

                # Remove invalid rows
                data = data.dropna(subset=['Target'])

                X = data.drop('Target', axis=1)
                y = data['Target']

                # Convert numeric
                X = X.apply(pd.to_numeric, errors='coerce')

                # Fill missing
                X.fillna(X.mean(), inplace=True)

                return X, y

            x_train, y_train = preprocess(train_data)
            x_test, y_test = preprocess(test_data)

            # ------------------ SELECT ONLY FORM FEATURES ------------------
            selected_features = [
                'Age', 'Gender', 'BMI', 'Systolic_BP', 'Diastolic_BP',
                'Heart_Rate', 'Sodium', 'Potassium', 'Hemoglobin',
                'Diabetes', 'Hypertension', 'Smoking_Status'
            ]

            x_train = x_train[selected_features]
            x_test = x_test[selected_features]

            # ------------------ MODELS ------------------

            from sklearn.tree import DecisionTreeClassifier
            dt_model = DecisionTreeClassifier(max_depth=4)
            dt_model.fit(x_train, y_train)
            dt_pred = dt_model.predict(x_test)

            from sklearn.ensemble import RandomForestClassifier
            rf_model = RandomForestClassifier(n_estimators=100, max_depth=5)
            rf_model.fit(x_train, y_train)
            rf_pred = rf_model.predict(x_test)

            from sklearn.linear_model import LogisticRegression
            lr_model = LogisticRegression()
            lr_model.fit(x_train, y_train)
            lr_pred = lr_model.predict(x_test)

            # ------------------ ACCURACY ------------------

            from sklearn.metrics import accuracy_score

            dt_acc = accuracy_score(y_test, dt_pred)
            rf_acc = accuracy_score(y_test, rf_pred)
            lr_acc = accuracy_score(y_test, lr_pred)

            # ------------------ USER INPUT ------------------

            input_df = pd.DataFrame([[
                age, gender, bmi, systolic_bp, diastolic_bp,
                heart_rate, sodium, potassium, hemoglobin,
                diabetes, hypertension, smoking
            ]], columns=selected_features)

            # ------------------ PREDICTIONS ------------------

            dt_result = dt_model.predict(input_df)[0]
            rf_result = rf_model.predict(input_df)[0]
            lr_result = lr_model.predict(input_df)[0]

            # Label mapping
            label_map = {
                0: "Healthy Kidney",
                1: "Mild CKD",
                2: "Moderate CKD",
                3: "Severe CKD"
            }

            dt_result = label_map[dt_result]
            rf_result = label_map[rf_result]
            lr_result = label_map[lr_result]

            # ------------------ BEST MODEL ------------------

            max_acc = max(dt_acc, rf_acc, lr_acc)

            best_models = []

            if dt_acc == max_acc:
                best_models.append("Decision Tree")

            if rf_acc == max_acc:
                best_models.append("Random Forest")

            if lr_acc == max_acc:
                best_models.append("Logistic Regression")

            # Convert list to string
            best_model = ", ".join(best_models)

            # ------------------ CONTEXT ------------------

            context = {
                "dt_result": dt_result,
                "rf_result": rf_result,
                "lr_result": lr_result,

                "dt_acc": round(dt_acc * 100, 2),
                "rf_acc": round(rf_acc * 100, 2),
                "lr_acc": round(lr_acc * 100, 2),

                "best_model": best_model,
                "show_result": True
            }

            return render(request, "ckd_prediction.html", context)

    return render(request, "ckd_prediction.html")



def signup(request):
    if (request.method=="POST"):
        uname=request.POST.get("username")
        email=request.POST.get("email")
        pass1=request.POST.get("password1")
        pass2=request.POST.get("password2")
        if pass1!=pass2:
            return HttpResponse("Password and Confirm Password are not same")
        else:
            my_user=User.objects.create_user(uname,email,pass1)
            my_user.save()
            return redirect('login')
    return render(request,"signup.html")



def Login(request):
    if(request.method=="POST"):
        username=request.POST.get("username")
        password=request.POST.get("pass")
        user=User.objects.filter(username=username)
        user=authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect('index')
        else:
            return render(request,"login.html",{"error": "Invalid username or password"})
    return render(request, "login.html")        


def Logout(request):
    logout(request)
    return redirect('login')
    