import React from 'react';
import ReactApexChart from 'react-apexcharts';


const options = {
  chart: {
    type: 'candlestick',
    height: 350
  },
  title: {
    text: 'CandleStick Chart',
    align: 'left'
  },
  xaxis: {
    type: 'datetime'
  },
  yaxis: {
    tooltip: {
      enabled: true
    }
  }
};

export default function CandlestickChart( data ) {
  const series = [
    data
  ];
  
  return (
    <div>
      <div id="chart">
        <ReactApexChart 
        options={options} 
        series={series} 
        type="candlestick" 
        height={350} />
      </div>
    </div>
  );
}