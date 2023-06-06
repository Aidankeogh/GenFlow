console.log('aloha', tables.xgboost_mass_fullsweep_exp[0])
console.log('aloha keys', Object.keys(tables.xgboost_mass_fullsweep_exp[0]))
let seriesRef = {
    "xgboost_mass_fullsweep_exp": {
        symbolSize: 10,
        "data": [],
        "name": "XGBoost Mass Fullsweep Experiment",
        "type": "scatter"
    },
}

tables.xgboost_mass_fullsweep_exp.forEach(row => {
    let val = {
        value: [parseFloat(row.param_model_params_lambda), parseFloat(row.metric_R2_mean)],
        row: row
    }
    seriesRef["xgboost_mass_fullsweep_exp"].data.push(val)
})

const showAsInTooltip = {
    run_name: "Name",
    metric_R2_mean: "R2 Mean",
    param_model_params_lambda: "Lambda",
}
function tooltipFormatter(p){
    let tooltipHtml = `<span>${p.marker} ${p.seriesName}</span>`;
    Object.keys(showAsInTooltip).forEach(key => {
        tooltipHtml += `<br><span><strong>${showAsInTooltip[key]}</strong> ${p.data.row[key]}</span>`;
    });

    return tooltipHtml;
}

option = {
    title: {
      "text": "XGBoost Mass Fullsweep Experiment",
      "left": "center"
    },
    xAxis: {
        "label": "Model Lambda"
    },
    yAxis: {
        "label": "R2 Mean"
    },
    tooltip: {
        show: true,
        formatter: tooltipFormatter
    },
    series: [
        seriesRef["xgboost_mass_fullsweep_exp"]
    ]
};
return option;