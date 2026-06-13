pipeline {
    agent any

    triggers {
        pollSCM('H/5 * * * *')
    }

    options {
        skipDefaultCheckout(false)
    }

    stages {

        stage('Set up environment') {
            steps {
                sh '''
                    python3 -m venv .venv
                    . .venv/bin/activate
                    pip install --upgrade pip
                    pip install . -r requirements.txt
                '''
            }
        }

        stage('Lint (ruff)') {
            steps {
                sh '. .venv/bin/activate && ruff check .'
            }
        }

        stage('Tests (pytest)') {
            steps {
                sh '. .venv/bin/activate && pytest --junitxml=report.xml'
            }
            post {
                always {
                    junit 'report.xml'
                }
            }
        }

        stage('Build artifact (wheel)') {
            steps {
                sh '. .venv/bin/activate && python -m build --wheel'
                archiveArtifacts artifacts: 'dist/*.whl', fingerprint: true
            }
        }

        stage('Local deploy + smoke test') {
            steps {
                sh '''
                    . .venv/bin/activate
                    uvicorn app.main:app --host 127.0.0.1 --port 8000 &
                    APP_PID=$!
                    sleep 3
                    curl -fsS http://127.0.0.1:8000/health
                    RESULT=$?
                    kill $APP_PID || true
                    exit $RESULT
                '''
            }
        }
    }

    post {
        success { echo 'Pipeline OK - build is ready.' }
        failure { echo 'Pipeline FAILED - check the stage logs.' }
    }
}