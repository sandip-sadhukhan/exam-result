const rollNumberUI = document.getElementById('roll_number');
const submitBtnUI = document.getElementById('submitbtn');
const semUI = document.getElementById('sem')
const homePage = document.getElementById('homepage');
const resultPage = document.getElementById('resultpage');
const resetBtnUI = document.getElementById('resetBtn');
const downloadBtnUI = document.getElementById('downloadBtn');
const resultName = document.getElementById('result-name');
const resultRollNo = document.getElementById('result-rollno');
const resultCgpa = document.getElementById('result-cgpa');
const resultSem = document.getElementById('result-sem');

// Download global details
downloadFileName = ''
downloadFileURL = ''

// Dependent Functions
const ready = () => {
    rollNumberUI.focus();
}

const downloadPdf = () => {
    let link = document.createElement('a');
    link.href = downloadFileURL;
    link.download = downloadFileName;
    link.dispatchEvent(new MouseEvent('click'));
}

// downloadPdf(`../pdfs/${rollNumber}_marksheet.pdf`, rollNumber);

const submitBtnHandler = async()  => {
    let rollNumber = rollNumberUI.value;
    let sem = semUI.value;
    // validation
    if(rollNumber === ''){
        return;
    }
    fetch(`./../studentInfo/studentInfo.json`)
        .then(res => res.json())
        .then(data => {
            // update the result page
            semData = data[sem]
            result = semData[rollNumber]
            resultName.innerText = result['name'];
            resultRollNo.innerText = result['rollNo'];
            resultCgpa.innerText = result['cgpa'];
            resultSem.innerText = sem.slice(-2)
            // Update download links
            downloadFileName = result['name'] + `_${sem}`;
            downloadFileURL = `./../results/${sem}/${result['rollNo']}_marksheet.pdf`; 
            // home page vanish and result page shown
            homePage.style.display="none";
            resultPage.style.display="flex";
        })
        .catch(error => {console.log("Data not found!")});
}

const resetBtnHandler = () => {
    // Clear the input
    rollNumberUI.value = '';
    // home page shown and result page vanish
    resultPage.style.display="none";
    homePage.style.display="flex";
}

submitBtnUI.addEventListener('click', (e)=>{
    e.preventDefault();
    submitBtnHandler(); 
});

resetBtnUI.addEventListener('click', resetBtnHandler);
downloadBtnUI.addEventListener('click', downloadPdf);