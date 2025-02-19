pipeline {
    agent any

    environment {
        IMAGE_DIR = "./images"
        SAMPLE_IMAGE = "./sample.png"
        REFERENCE_IMAGE = "./image.png"
        RESULTS_DIR = "./Results"
        CLEANED_RESULTS_DIR = "./cleanedResults"
        ZIP_FILE = "results.zip"
        EMAIL_TO = "recipient@example.com" //*
    }

    stages {
        stage('Find Similar Images') {
            steps {
                script {
                    sh 'python3 find_similar.py'
                }
            }
        }

        stage('Archive Results') {
            steps {
                script {
                    sh "zip -r ${ZIP_FILE} ${RESULTS_DIR}"
                }
            }
        }

        stage('Send Email with ZIP') {
            steps {
                script {
                    emailext subject: "Search results for photos",
                              body: "The results of searching in the attachment.",
                              to: EMAIL_TO,
                              attachLog: false,
                              attachmentsPattern: ZIP_FILE
                }
            }
        }

        stage('Extract Matching Regions') {
            steps {
                script {
                    sh 'python3 extract_images.py'
                }
            }
        }
    }
}

