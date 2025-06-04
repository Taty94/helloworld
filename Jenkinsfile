pipeline {
    agent none
    options { skipDefaultCheckout() }
    stages {
        stage ('Get Code') {
            agent {label 'windows-agent'}
            steps {
                echo "=== Get Code ==="
                printAgentInfo()
                // Get the code from GitHub
                git branch: 'feature_fix_coverage', url: 'https://github.com/Taty94/helloworld.git'
                bat 'dir'
                echo WORKSPACE
                stash name:'code', includes:'**'
            }
        }

        stage ('Tests') {
            parallel {
                stage ('Unit & Coverage Analisys') {
                    agent {label 'python-tester'}
                    steps {
                        catchError(buildResult: 'UNSTABLE', stageResult: 'FAILURE') {
                            unstash 'code'
                            echo "===Unit & Coverage Analisys ==="
                            printAgentInfo()
                            sh '''
                                ls -la
                                export PYTHONPATH=.
                                coverage run --branch --source=app --omit=app/__init__.py,app/api.py -m pytest --junitxml=result-unit.xml test/unit/
                                coverage xml
                                coverage report
                            '''
                            junit 'result-unit.xml'
                            
                            cobertura coberturaReportFile: 'coverage.xml',
                                lineCoverageTargets: '95,0,85',
                                conditionalCoverageTargets: '90,0,80',
                                onlyStable: false
                            stash name:'unit', includes:'result-unit.xml'
                        }
                    }
                    post {
                        always {
                            cleanWs()
                        }
                    }
                }
                
                stage('Static') {
                    agent { label 'python-tester' }
                    steps {
                        unstash 'code'
                        echo "=== Static ==="
                        printAgentInfo()
                        sh '''
                            flake8 --format=pylint --exit-zero app >flake8.out
                        '''
                        recordIssues tools: [flake8(name: 'Flake8', pattern: 'flake8.out')],
                            qualityGates: [
                                [threshold: 8, type: 'TOTAL', unstable: true],
                                [threshold: 10, type: 'TOTAL', unstable: false]
                            ]
                    }
                    post {
                        always {
                            cleanWs()
                        }
                    }
                }
                
                stage('Security') {
                    agent { label 'python-tester' }
                    steps {
                        unstash 'code'
                        echo "=== Security ==="
                        printAgentInfo()
                        sh 'bandit --exit-zero -r . -f custom -o bandit.out --msg-template "{abspath}:{line}: [{test_id}] {msg}"'
                        recordIssues tools: [pyLint(name: 'Bandit', pattern: 'bandit.out')],
                            qualityGates: [
                                [threshold: 2, type: 'TOTAL', unstable:true],
                                [threshold: 4, type: 'TOTAL', unstable:false]
                            ]
                    }
                    post {
                        always {
                            cleanWs()
                        }
                    }
                }
                
                stage ('Rest') {
                    agent { label 'web-tester' }
                    steps {
                        catchError(buildResult: 'UNSTABLE', stageResult: 'FAILURE') {
                            unstash 'code'
                            echo "=== Rest ==="
                            printAgentInfo()
                            sh '''
                                export FLASK_APP=app/api.py
                                flask run &
                                sleep 4
                                java -jar /wiremock-standalone.jar --port 9090 --root-dir test/wiremock &
                                sleep 7
                                pytest --junitxml=result-rest.xml test/rest/
                                
                                lsof -t -i :5000 | xargs kill || true
                                lsof -t -i :9090 | xargs kill || true
                            '''
                            junit 'result-rest.xml'
                        }
                    }
                    post {
                        always {
                            cleanWs()
                        }
                    }
                }
            }
        }
        
        stage('Performance') {
            agent { label 'web-tester' }
            steps {
                    unstash 'code'
                    echo "=== Performance ==="
                    printAgentInfo()
                    sh '''
                        export FLASK_APP=app/api.py
                        flask run &
                        sleep 4
                        /opt/jmeter/bin/jmeter.sh -n -t test/jmeter/flask.jmx -f -l flask.jtl
                        lsof -t -i :5000 | xargs kill || true
                    '''
                    perfReport sourceDataFiles: 'flask.jtl'
                }
            post {
                always {
                    cleanWs()
                }
            }
        }
    }
}
def printAgentInfo() {
    def whoami
    def hostname
    def workspace = env.WORKSPACE

    if (isUnix()) {
        whoami = sh(script: 'whoami', returnStdout: true).trim()
        hostname = sh(script: 'hostname', returnStdout: true).trim()
    } else {
        whoami = bat(script: 'whoami', returnStdout: true).trim()
        hostname = bat(script: 'hostname', returnStdout: true).trim()
    }

    def box = """ 
    +-----------------------------------+ 
    |          Pipeline Info           | 
    +-----------------------------------+ 
    | User:      ${whoami}             | 
    | Hostname:  ${hostname}           | 
    | Workspace: ${workspace}          | 
    +-----------------------------------+ 
    """ 
    echo box
}