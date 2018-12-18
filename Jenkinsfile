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
    projectName = 't4-geom-convert'
    SRC = "${env.WORKSPACE}/src"
    VENV = "${env.WORKSPACE}/venv"
    ORACLE_BUILD = "${env.WORKSPACE}/oracle-build"
    DATA = "${SRC}/Oracle/data"
  }

  stages {
    stage('Checkout') {
      steps {
        dir("${SRC}") {
          checkout scm
        }
      }
    }
    stage('Configure') {
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
    stage('Build') {
      steps {
        echo "Starting cmake for ${env.BUILD_ID} on ${env.JENKINS_URL}..."
        dir("${ORACLE_BUILD}") {
          sh """
          make
          """
        }       
      }
    }
//     stage('Linting') {
//       steps {
//         echo 'Linting...'
//         dir("${SRC}") {
//           sh """
//               source "${VENV}/bin/activate"
//               pylint -f parseable valjean/ tests/ | tee pylint.out
//               # flake8 returns 1 in case of warnings and that would stop the
//               # build
//               flake8 --tee --output-file flake8.out || true
//               # avoid empty flake8.out files, Jenkins complains 
//               echo "end of flake8 file" >> flake8.out
//               """
//         }
//       }
//     }
//     stage('Build and check HTML doc') {
//       steps {
//         echo 'Building and checking documentation...'
//         dir("${SRC}") {
//           sh """
//              source "${VENV}/bin/activate"
//              # be nitpicky on the HTML documentation
//              PYTHONPATH=. sphinx-build -a -E -N -n -w sphinx-html.out -W -b html doc/src doc/build/html
//              PYTHONPATH=. sphinx-build -a -E -N -w sphinx-linkcheck.out -W -b linkcheck doc/src doc/build/linkcheck
//              """
//         }
//       }
//     }
    stage('Run unit tests') {
      steps {
        echo 'Running unit tests...'
        dir("${ORACLE_BUILD}") {
          sh """
						 cp ${DATA}/* ${ORACLE_BUILD}
						 ./tests --gtest_output=xml:gtestresults.xml
             """
//          step([$class: 'CoberturaPublisher',
//                autoUpdateHealth: false,
//                autoUpdateStability: false,
//                coberturaReportFile: 'tests/coverage.xml',
//                failUnhealthy: false,
//                failUnstable: false,
//                maxNumberOfBuilds: 0,
//                onlyStable: false,
//                sourceEncoding: 'ASCII',
//                zoomCoverageChart: false])
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
//      warnings(parserConfigurations: [[parserName: 'pep8', pattern: "**/flake8.out"],
//                                      [parserName: 'pylint', pattern: "**/pylint.out"],
//                                      [parserName: 'sphinx-build', pattern: "**/sphinx-html.out"],
//                                      [parserName: 'sphinx-linkcheck', pattern: "**/sphinx-linkcheck.out"]],
//               usePreviousBuildAsReference: true)
//      archiveArtifacts artifacts: "**/flake8.out", fingerprint: true
//      archiveArtifacts artifacts: "**/pylint.out", fingerprint: true
//      archiveArtifacts artifacts: "**/sphinx-html.out", fingerprint: true
//      archiveArtifacts artifacts: "**/sphinx-linkcheck.out", fingerprint: true
//      archiveArtifacts artifacts: "**/pytest.out", fingerprint: true
//      publishHTML (target: [
//                   allowMissing: false,
//                   alwaysLinkToLastBuild: false,
//                   keepAll: true,
//                   reportDir: "${SRC}/doc/build/html",
//                   reportFiles: 'index.html',
//                   reportName: "Sphinx documentation"
//      ])
      junit "**/gtestresults.xml"
    }
    cleanup {
      cleanWs()
    }
  }
}
