pipeline {
    agent any

    environment {
        IMAGE_NAME = "abakhar217/flask-service:flask-service-${BUILD_NUMBER}"
    }

    stages {
        stage('Checkout') {
            steps {
                // Checkout the code from the repository using the configured Git credentials
                checkout([$class: 'GitSCM',
                          branches: [[name: 'main']],
                          userRemoteConfigs: [[url: 'https://github.com/InvestBuddy/Machine-Learning.git', credentialsId: 'git']]])
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    // Build the Docker image with the .jar file inside the image
                    bat "docker build -t ${IMAGE_NAME} ."
                }
            }
        }

        stage('Push Docker Image') {
            steps {
                script {
                    // Use the credentials stored in Jenkins for Docker Hub
                    withCredentials([usernamePassword(credentialsId: 'dockerhub', passwordVariable: 'DOCKER_PASSWORD', usernameVariable: 'DOCKER_USERNAME')]) {
                        // Log in to Docker Hub
                        bat "echo %DOCKER_PASSWORD% | docker login -u %DOCKER_USERNAME% -p %DOCKER_PASSWORD% "
                        // Push the image to Docker Hub
                        bat "docker push ${IMAGE_NAME}"
                    }
                }
            }
        }

	stage('Deploy to Kubernetes') {
	    steps {
	        script {
	           // Replace a placeholder in user-service.yml with the build number
	          if (isUnix()) {
	             sh "sed -i 's#<BUILD_NUMBER>#${BUILD_NUMBER}#g' flask-service.yml"
	           } 
			   else {
	               bat "powershell -Command \"(Get-Content ${WORKSPACE}/flask-service.yml) -replace '<BUILD_NUMBER>', '${BUILD_NUMBER}' | Set-Content ${WORKSPACE}/flask-service.yml\""
	           }
	            withKubeConfig([credentialsId: 'kubectl']) {
	              if (isUnix()) {
	                sh 'kubectl apply -f flask-service.yml'
	             } else {
	                bat 'kubectl apply -f flask-service.yml'
	               }
	             }
	          }
	     }
	}

	    
    }

	post {
	    always {
	        echo "Pipeline completed. Final status: ${currentBuild.currentResult}"
	        bat 'docker system prune -f'
	    }
	    success {
	        echo "Pipeline succeeded! Build number: ${env.BUILD_NUMBER}, Job name: ${env.JOB_NAME}"
	    }
	    unstable {
	        echo "Pipeline marked as UNSTABLE. Possible cause: Quality Gate failure or warnings."
	    }
	    failure {
	        echo "Pipeline failed!"
	        echo "Error Details: ${currentBuild.description ?: 'No detailed error provided.'}"
	        script {
	            currentBuild.description = "Failure occurred during ${env.STAGE_NAME}. Check logs."
	        }
	    }
	    aborted {
	        echo "Pipeline was aborted by user or timeout."
	    }
	}


}
