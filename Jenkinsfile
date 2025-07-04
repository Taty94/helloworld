pipeline {
    agent any
    options { skipDefaultCheckout() }
    stages {
        stage ('Get Code') {
            steps {
                // Get the code from GitHub
                git url: 'https://github.com/Taty94/helloworld.git'
                bat 'dir'
                echo WORKSPACE
            }
        }

        stage ('Tests') {
            parallel {
                stage ('Unit & Coverage') {
                    steps {
                        catchError(buildResult: 'UNSTABLE', stageResult: 'FAILURE') {
                            bat '''
                                set PYTHONPATH=.
                                coverage run --branch --source=app --omit=app\\__init__.py,app\\api.py -m pytest --junitxml=result-unit.xml  test\\unit
                                coverage xml
                                coverage report
                            '''
                            cobertura coberturaReportFile: 'coverage.xml',
                                lineCoverageTargets: '95,0,85', 
                                conditionalCoverageTargets: '90,0,80',
                                onlyStable: false,
                                autoUpdateStability: true
                                
                            junit 'result-unit.xml'
                        }
                    }
                }

                stage ('Rest') {
                    steps {
                        catchError(buildResult: 'UNSTABLE', stageResult: 'FAILURE') {
                            bat '''
                                set FLASK_APP=app\\api.py
                                start flask run
                                start java -jar C:\\TATIANA\\UNIR\\Modulo2\\CP1-A\\helloworld\\test\\wiremock\\wiremock-standalone-4.0.0-beta.2.jar --port 9090 --root-dir test\\wiremock
                                
                                python C:\\TATIANA\\UNIR\\Modulo2\\CP1-A\\helloworld\\check_servers.py
                            
                                pytest --junitxml=result-rest.xml test\\rest
                            '''
                            junit 'result-rest.xml'
                        }
                    }
                }
            }
        }
        
        stage('Static') {
                steps {
                    bat '''
                        flake8 --format=pylint --exit-zero app >flake8.out
                    '''
                    recordIssues tools: [flake8(name: 'Flake8', pattern: 'flake8.out')], 
                        qualityGates: [
                            [threshold: 8, type: 'TOTAL', unstable: true],
                            [threshold: 10, type: 'TOTAL', unstable: false]
                        ]
                }
        }
        
        stage('Security') {
            steps {
                bat '''
                    bandit --exit-zero -r . -f custom -o bandit.out --msg-template "{abspath}:{line}: [{test_id}] {msg}"
                '''
                recordIssues tools: [pyLint(name: 'Bandit', pattern: 'bandit.out')], 
                    qualityGates: [
                        [threshold: 2, type: 'TOTAL', unstable:true],
                        [threshold: 4, type: 'TOTAL', unstable:false]
                    ]
            }
        }

        stage('Performance') {
            steps {
                catchError(buildResult: 'UNSTABLE', stageResult: 'FAILURE') {
                    bat '''
                        set FLASK_APP=app\\api.py
                        start flask run
                        C:\\TATIANA\\UNIR\\Modulo2\\CP1-A\\apache-jmeter-5.6.3\\bin\\jmeter.bat -n -t test\\jmeter\\flask.jmx -f -l flask.jtl
                    '''
                    perfReport sourceDataFiles: 'flask.jtl'
                }
            }
        }
    }
}