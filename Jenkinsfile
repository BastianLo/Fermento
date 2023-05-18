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
                    echo env.GIT_BRANCH
                    echo GIT_BRANCH
                    if (GIT_BRANCH == 'main') {
                        sh 'docker tag fermento:$BUILD_ID bastianlo/fermento:latest'
                    }
                    sh "docker tag fermento:$BUILD_ID bastianlo/fermento:${env.BRANCH_NAME}"
                    sh 'docker push bastianlo/fermento --all-tags'
                }
            }
        }
    }
}