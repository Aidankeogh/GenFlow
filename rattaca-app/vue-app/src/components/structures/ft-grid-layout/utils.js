import vm from 'vm-browserify';

export const runJsCode = (js, args) => {
    const runCode = 
`function runSandBoxedCode(){
    ${js}
}

runSandBoxedCode();`;
    return vm.runInNewContext(runCode, args);
}


// let xAxisData = [];
// let lineSeries = {
//     name: 'Mean Squared Error',
//     type: 'line',
//     data: []
// };
// let barSeries = {
//     name: 'Test Size',
//     type: 'bar',
//     data: []
// };
// console.log(tables)
// tables.Housing.forEach((row) => {
//     lineSeries.data.push(row.metric_mean_squared_error);
//     barSeries.data.push(row.param_test_size);
//     xAxisData.push(row.run_name)
// })

// option = {
//     legend:{
//         show: true,
//         top: 'bottom',
//         left: 'center'
//     },
//   title: {
//     text: 'Housing Experiment',
//     left: 'center',
//     subtext: 'Mean Squared Error vs Test Size'
//   },
//   xAxis: {
//     type: 'category',
//     data: xAxisData
//   },
//   yAxis: {
//     type: 'value'
//   },
//   series: [
//     lineSeries,
//     barSeries
//   ]
// };
// return option;
