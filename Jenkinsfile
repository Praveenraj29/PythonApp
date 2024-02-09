pipeline {
    agent any
    stage('Env Var')
    {
        echo '${BUILD_NUMBER}'
    }
    stage('Docker Build') 
    {
      steps {
          sh 'docker build -t authapp:${BUILD_Number} .'
      }
    }
    stage('Docker Run')
    {
      steps{
        sh 'docker run -p 8000:8000 authapp:latest'
      }
    }
}
