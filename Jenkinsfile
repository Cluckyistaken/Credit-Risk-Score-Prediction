pipeline {
    agent any

    tools {
        // Make sure to configure a NodeJS installation named 'node-18' in Jenkins Global Tool Configuration
        nodejs 'node-18' 
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Backend Test') {
            steps {
                dir('backend') {
                    script {
                        // Check if running on Windows or Unix/Linux to use appropriate command
                        if (isUnix()) {
                            sh 'python3 -m venv venv'
                            sh '. venv/bin/activate && pip install -r requirements.txt'
                            sh '. venv/bin/activate && python manage.py test'
                        } else {
                            bat 'python -m venv venv'
                            bat 'call venv\\Scripts\\activate.bat && pip install -r requirements.txt'
                            bat 'call venv\\Scripts\\activate.bat && python manage.py test'
                        }
                    }
                }
            }
        }

        stage('Frontend Build') {
            steps {
                dir('frontend') {
                    script {
                        if (isUnix()) {
                            sh 'npm install'
                            sh 'npm run build'
                        } else {
                            bat 'npm install'
                            bat 'npm run build'
                        }
                    }
                }
            }
        }

        stage('Selenium Test') {
            steps {
                script {
                    // This stage assumes backend and frontend are running.
                    // In a real CI env, you'd start them here using background processes.
                    // For this simple setup, we'll just run the script assuming the env is ready 
                    // or use a simple check.
                    
                    dir('backend') {
                         if (isUnix()) {
                            sh '. venv/bin/activate && pip install selenium webdriver-manager'
                         } else {
                            bat 'call venv\\Scripts\\activate.bat && pip install selenium webdriver-manager'
                         }
                    }
                    
                    // Run the test script (at root)
                    // We use the backend venv to run the python script
                    if (isUnix()) {
                        sh 'backend/venv/bin/python selenium_test.py'
                    } else {
                        bat 'backend\\venv\\Scripts\\python.exe selenium_test.py'
                    }
                }
            }
        }
    }
}
