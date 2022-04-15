def notifyTuleap(boolean success) {
  String statusTag = "failure"
  if (success) {
    statusTag = "success"
  }
  REPO_ID=1076  // repository ID
  withCredentials([string(credentialsId: "ci-token-${REPO_ID}", variable: 'token')]) {
    sh """#!/bin/bash
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

  agent { label 'tripoli4' }

  parameters {
    booleanParam(name: 'WITH_ORACLE', defaultValue: false, description: 'If true, compile and run the test oracle')
  }

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
      when {
        equals expected: true, actual: params.WITH_ORACLE
      }
      steps {
        echo "Starting cmake for ${env.BUILD_ID} on ${env.JENKINS_URL}..."
        dir("${ORACLE_BUILD}") {
          sh """#!/bin/bash
          . /home/tri4dev/developers/prerequisites/install/lin-x86-64-cen7/root_v6.12.06/bin/thisroot.sh
          cmake3 ${SRC}/Oracle -DT4_DIR=/data/tmpdm2s/dm232107/product/t4/t4.11/cen7/share/cmake -DHDF5_DIR=/home/tri4dev/developers/prerequisites/install/lin-x86-64-cen7/hdf5-1.8.14
          """
        }
      }
    }
    stage('Build Oracle') {
      when {
        equals expected: true, actual: params.WITH_ORACLE
      }
      steps {
        echo "Starting cmake for ${env.BUILD_ID} on ${env.JENKINS_URL}..."
        dir("${ORACLE_BUILD}") {
          sh """#!/bin/bash
          make
          """
        }       
      }
    }
    stage('Install t4_geom_convert') {
      steps {
        sh """#!/bin/bash
        PYTHON=python3.8
        /usr/bin/which python3.6 && PYTHON=python3.6
        \${PYTHON} -m venv '${VENV}'
        . '${VENV}/bin/activate'
        \${PYTHON} -m pip install --upgrade pip setuptools
        \${PYTHON} -m pip install '${SRC}[dev]'
        """
      }
    }
    stage('Linting') {
      steps {
        echo 'Linting...'
        dir("${SRC}") {
          sh """#!/bin/bash
              . "${VENV}/bin/activate"
              pylint -f parseable t4_geom_convert/ | tee pylint.out || true
              """
        }
      }
    }
    stage('Run oracle unit tests') {
      when {
        equals expected: true, actual: params.WITH_ORACLE
      }
      steps {
        echo 'Running unit tests...'
        dir("${ORACLE_BUILD}") {
          sh """#!/bin/bash
             cp ${DATA}/* ${ORACLE_BUILD}
             ./tests --gtest_output=xml:gtestresults.xml
             """
        }
      }
    }
    stage('Run t4_geom_convert unit tests') {
      steps {
        echo 'Running unit tests...'
        dir("${SRC}") {
          sh """#!/bin/bash
             . "${VENV}/bin/activate"
             pytest --cov-report term-missing --cov-config .coveragerc --cov-report=xml --cov=t4_geom_convert --junit-xml=pytest.xml | tee pytest.out || true
             """
          step([$class: 'CoberturaPublisher',
                autoUpdateHealth: false,
                autoUpdateStability: false,
                coberturaReportFile: 'coverage.xml',
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
      dir("${SRC}") {
        recordIssues enabledForFailure: true, tool: pyLint(pattern: '**/pylint.out', reportEncoding: 'UTF-8')
      }
      archiveArtifacts artifacts: "**/pylint.out", fingerprint: true
      archiveArtifacts artifacts: "**/pytest.out", fingerprint: true
      junit "**/pytest.xml"
    }
  }
}
