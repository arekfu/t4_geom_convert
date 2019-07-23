def notifyTuleap(boolean success) {
  String statusTag = "failure"
  if (success) {
    statusTag = "success"
  }
  REPO_ID=1076  // repository ID
  withCredentials([string(credentialsId: "ci-token-${REPO_ID}", variable: 'token')]) {
    sh """
       cd ${SRC}
       rev="\$(git rev-parse HEAD)"
       curl -k "https://codev-tuleap.intra.cea.fr/api/git/${REPO_ID}/statuses/\$rev" \
       -X POST \
       -H 'Content-Type: application/json' \
       -H 'Accept: application/json' \
       --data-binary "{ \\"state\\": \\"$statusTag\\", \\"token\\": \\"$token\\"}"
       """
  }
}

pipeline {
  options {
    skipDefaultCheckout()
    timestamps()
    timeout(time: 1, unit: 'HOURS')
  }

  agent { label 'T4' }

  environment {
    projectName = 't4_geom_convert'
    SRC = "${env.WORKSPACE}/src"
    VENV = "${env.WORKSPACE}/venv"
    ORACLE_BUILD = "${env.WORKSPACE}/oracle-build"
    DATA = "${SRC}/Oracle/data"
  }

  stages {
    stage('Clean workspace') {
      steps {
        cleanWs()
      }
    }
    stage('Checkout') {
      steps {
        dir("${SRC}") {
          checkout scm
        }
      }
    }
    stage('Configure Oracle') {
      steps {
        echo "Starting cmake for ${env.BUILD_ID} on ${env.JENKINS_URL}..."
        dir("${ORACLE_BUILD}") {
          sh """
          . /home/tri4dev/developers/prerequisites/install/lin-x86-64-cen7/root_v6.12.06/bin/thisroot.sh
          cmake3 ${SRC}/Oracle -DT4_DIR=/data/tmpdm2s/dm232107/product/t4/t4.11/cen7/share/cmake -DHDF5_DIR=/home/tri4dev/developers/prerequisites/install/lin-x86-64-cen7/hdf5-1.8.14
          """
        }
      }
    }
    stage('Build Oracle') {
      steps {
        echo "Starting cmake for ${env.BUILD_ID} on ${env.JENKINS_URL}..."
        dir("${ORACLE_BUILD}") {
          sh """
          make
          """
        }       
      }
    }
    stage('Install Converter') {
      steps {
        sh """
        python3 -m venv "${VENV}"
        source "${VENV}/bin/activate"
        python3 -m pip install --upgrade pip setuptools
        python3 -m pip install ${SRC}[dev]
        """
      }
    }
    stage('Linting') {
      steps {
        echo 'Linting...'
        dir("${SRC}") {
          sh """
              source "${VENV}/bin/activate"
              pylint -f parseable t4_geom_convert/ | tee pylint.out || true
              # flake8 returns 1 in case of warnings and that would stop the
              # build
              flake8 --tee --output-file flake8.out t4_geom_convert/ || true
              # avoid empty flake8.out files, Jenkins complains 
              echo "end of flake8 file" >> flake8.out
              """
        }
      }
    }
    stage('Run unit tests') {
      steps {
        echo 'Running unit tests...'
        dir("${ORACLE_BUILD}") {
          sh """
             cp ${DATA}/* ${ORACLE_BUILD}
             ./tests --gtest_output=xml:gtestresults.xml
             """
        }
        dir("${SRC}") {
          sh """
             source "${VENV}/bin/activate"
             pytest --cov-report term-missing --cov-config .coveragerc --cov-report=xml --cov=t4_geom_convert --junit-xml=pytest.xml --timeout=30 | tee pytest.out || true
             """
          step([$class: 'CoberturaPublisher',
                autoUpdateHealth: false,
                autoUpdateStability: false,
                coberturaReportFile: 'UnitTests/coverage.xml',
                failUnhealthy: false,
                failUnstable: false,
                maxNumberOfBuilds: 0,
                onlyStable: false,
                sourceEncoding: 'ASCII',
                zoomCoverageChart: false])
        }
      }
    }
  }
  post {
    success {
        notifyTuleap(true)
    }
    failure {
        notifyTuleap(false)
    }
    always {
      recordIssues referenceJobName: 'valjean/reference/master', enabledForFailure: true, tool: pep8(pattern: '**/flake8.out', reportEncoding: 'UTF-8')
      recordIssues referenceJobName: 'valjean/reference/master', enabledForFailure: true, tool: pyLint(pattern: '**/pylint.out', reportEncoding: 'UTF-8')
      archiveArtifacts artifacts: "**/flake8.out", fingerprint: true
      archiveArtifacts artifacts: "**/pylint.out", fingerprint: true
      archiveArtifacts artifacts: "**/pytest.out", fingerprint: true
      junit "**/pytest.xml"
    }
  }
}
