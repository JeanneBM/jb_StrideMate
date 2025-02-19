pipeline {
    agent any

    environment {
        IMAGE_DIR = "./images"
        SAMPLE_IMAGE = "./sample.png"
        REFERENCE_IMAGE = "./image.png"
        RESULTS_DIR = "./Results"
        CLEANED_RESULTS_DIR = "./cleanedResults"
    }

    stages {
        stage('Find Similar Images') {
            steps {
                script {
                    sh 'python3 find_similar.py'
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
