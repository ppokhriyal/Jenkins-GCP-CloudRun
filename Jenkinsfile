pipeline{
    agent any
    parameters {
        string defaultValue: 'jenkins-377105', description: 'GCP Project ID', name: 'projectid'
    }
    environment{
        SERVICE_ACCOUNT_EMAIL="jenkins@jenkins-377105.iam.gserviceaccount.com"
    }
    stages{
        stage("Check GCLOUD Version"){
            steps{
                sh '''
                    gcloud --version
                '''
            }
        }
        stage("Set GCP Project"){
            steps{
                sh '''
                    gcloud config set project $projectid
                '''
            }
        }
        stage("GCP Authentication"){
            steps{
                withCredentials([file(credentialsId: 'gcloud-creds', variable: 'GCLOUD_CREDS')]) {
                    sh ''' 
                        gcloud auth activate-service-account --key-file="$GCLOUD_CREDS"
                    '''
                }
            }
        }
        stage("Create GCP Artifact Repository"){
            steps{
                script{
                    sh '''
                        gcloud artifacts repositories create vanilla-artifact --location us-central1 --repository-format=docker || true
                       '''
                }
            }
        }
        stage("Build Docker Image"){
		steps{
                	sh ''' 
                    		docker build -t us-central1-docker.pkg.dev/jenkins-377105/vanilla-artifact/vanilla-image:"$GIT_COMMIT" .
                	'''
            	}
        }
	stage("Push Docker Image to GCP Artifact Registry"){
		steps{
			sh '''
				echo Y | gcloud auth configure-docker us-central1-docker.pkg.dev
				docker push us-central1-docker.pkg.dev/"$projectid"/vanilla-artifact/vanilla-image:"$GIT_COMMIT"
			 '''	
		}
	}
	stage("Deploy Docker image to Cloud Run"){
		steps{
			sh ''' 
				gcloud run deploy vanilla-cloudrun --image=us-central1-docker.pkg.dev/jenkins-377105/vanilla-artifact/vanilla-image:"$GIT_COMMIT" --max-instances=5 --min-instances=1 --region=us-central1 --allow-unauthenticated
			'''
		}
	}
    }
    post {
        always {
            sh '''
            gcloud auth revoke "$SERVICE_ACCOUNT_EMAIL"
            '''
        }
    }
}
