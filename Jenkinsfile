pipeline {
    agent any
    options {
        buildDiscarder(logRotator(numToKeepStr: '5', daysToKeepStr: '5'))
        timestamps()
    }
    environment {
        DOCKERHUB_COMMON_CREDS = credentials('jenkins-dockerhub-common-creds')
    }
    stages {
        stage('Building image') {
            steps {
                script {
                    sh 'docker build -t bastianlo/fermento:$BUILD_ID -t bastianlo/fermento:latest -t fermento:${BUILD_ID} .'
                }
            }
        }
        stage('Deploy Image') {
            steps {
                script {
                    sh '''  docker login --username=$DOCKERHUB_COMMON_CREDS_USE --password=$DOCKERHUB_COMMON_CREDS_PSW
                            docker tag fermento:$BUILD_ID bastianlo/fermento:$BUILD_ID
                            docker tag fermento:$BUILD_ID bastianlo/fermento:latest
                            docker push bastianlo/fermento'''
                    }
                }
            }
        }
    }
}