pipeline {
    agent any
    stages {
        stage ('Get Code') {
            steps {
                echo 'Pipe started: Running a simple stage with echo'
                //Get the code from GitHub
                echo 'Cloning the repo ...'
                git url: 'https://github.com/Taty94/helloworld.git'
                //Show the downloeaden files
                echo 'Verifying that the code has been downloaded'
                bat 'dir'
                //Show the WORSPACE
                echo "The Workspace is: ${env.WORKSPACE}"

            }
        }

        stage ('Build'){
            steps {
                echo "Build Stage: doen't do anything!"
            }
        }
    }
}