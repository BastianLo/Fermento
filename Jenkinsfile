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
                    sh 'docker login --username=$DOCKERHUB_COMMON_CREDS_USR --password=$DOCKERHUB_COMMON_CREDS_PSW'
                    sh 'docker tag fermento:$BUILD_ID bastianlo/fermento:$BUILD_ID'
                    sh 'docker tag fermento:$BUILD_ID bastianlo/fermento:latest'
                    sh 'docker push bastianlo/fermento --all-tags'
                }
            }
        }
    }
}