pipeline {
    agent {
        docker { image 'node:20.11.0-alpine3.19' }
    }
    stages {
        stage('BUILD NUM') {
            steps {
                echo '${BUILD_NUMBER}'
            }
        }
        stage('Dir') {
          steps {
            sh 'ls -a'
          }
        }
        stage('Docker Build') {
            steps {
                sh 'docker build -t authapp .'
            }
        }
        stage('Docker Run') {
            steps {
                sh 'docker run -p 8000:8000 authapp'
            }
        }
    }
}
