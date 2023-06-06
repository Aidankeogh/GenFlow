// xgboost_m_fs_alpha_lambda

function getBubbleSize(dataItem, params){
    let r2 = 0
    try{
        r2 = parseFloat(params.data.row.metric_R2_mean);
    }
    catch(err){}
    if(r2 <= 0){
        return 1
    }
    return 200*r2;
}

let seriesRef = {
    "xgboost_mass_fullsweep_exp": {
        symbolSize: getBubbleSize,
        "data": [],
        "name": "XGBoost Mass Fullsweep Experiment",
        "type": "scatter"
    },
}

tables.xgboost_mass_fullsweep_exp.forEach(row => {
    let val = {
        value: [parseFloat(row.param_model_params_lambda), parseFloat(row.param_model_params_alpha), parseFloat(row.metric_R2_mean)],
        row: row
    }
    seriesRef["xgboost_mass_fullsweep_exp"].data.push(val)
})

const showAsInTooltip = {
    run_name: "Name",
    metric_R2_mean: "R2 Mean",
    param_model_params_lambda: "Lambda",
    param_model_params_alpha: "Alpha"
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
        "name": "Model Lambda"
    },
    yAxis: {
        "name": "Model Alpha"
    },
    tooltip: {
        show: true,
        formatter: tooltipFormatter
    },
    series: [
        seriesRef["xgboost_mass_fullsweep_exp"]
    ],
    visualMap: {
        bottom: 14,
        left: "center",
        calculable: true,
        min: 0,
        max: 0.25,
        type: "piecewise",
        orient: "horizontal"
    }
};
return option;


// tables spec

