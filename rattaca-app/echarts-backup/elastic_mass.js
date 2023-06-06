// optuna_elastic_mass

function getBubbleSize(dataItem, params){
    let r2 = 0
    try{
        r2 = parseFloat(params.data.row.metric_R2_mean);
    }
    catch(err){}
    if(r2 <= 0){
        return 1
    }
    return 200*(r2);
}

let seriesRef = {
    "optuna_elastic_mass": {
        symbolSize: getBubbleSize,
        "data": [],
        "name": "Elastic Experiment",
        "type": "scatter"
    },
}

tables.optuna_elastic_mass.forEach(row => {
    let val = {
        value: [parseFloat(row.param_model_params_l1_ratio), parseFloat(row.param_model_params_alpha), parseFloat(row.metric_R2_mean)],
        row: row
    }
    seriesRef["optuna_elastic_mass"].data.push(val)
})

const showAsInTooltip = {
    run_name: "Name",
    metric_R2_mean: "R2 Mean",
    param_model_params_l1_ratio: "Lambda",
    param_model_params_alpha: "Alpha"
}
function tooltipFormatter(p){
    let tooltipHtml = `<span>${p.marker} ${p.seriesName}</span>`;
    Object.keys(showAsInTooltip).forEach(key => {
        tooltipHtml += `<br><span><strong>${showAsInTooltip[key]}</strong> ${p.data.row[key]}</span>`;
    });

    return tooltipHtml;
}

function visualmapFormatter(value){
    return `${value.toFixed(3)}`;
}

option = {
    title: {
      "text": "Elastic Experiment",
      "left": "center"
    },
    xAxis: {
        "name": "Model L1",
    },
    yAxis: {
        "name": "Model Alpha",
    },
    tooltip: {
        show: true,
        formatter: tooltipFormatter,
        position: "inside"
    },
    series: [
        seriesRef["optuna_elastic_mass"]
    ],
    visualMap: {
        color:["#5e3c99", "#b2abd2", "#fdb863", "#e66101"],
        splitNumber: 7,
        left: "left",
        top: "middle",
        calculable: true,
        min: 0.01,
        max: 0.26,
        type: "continuous",
        orient: "vertical",
        formatter: visualmapFormatter
    },
    dataZoom: [
        {
          type: 'slider',
          show: true,
          xAxisIndex: [0]
        },
        {
          type: 'slider',
          show: true,
          yAxisIndex: [0]
        },
        {
          type: 'inside',
          xAxisIndex: [0]
        },
        {
          type: 'inside',
          yAxisIndex: [0]
        }
    ],
};
return option;