// src/components/TickerPortfolio.js
import React, { useState, useEffect } from 'react';

import { Box, List, Card, Grid, ListItem, Typography, ListItemText } from '@mui/material';

import CandlestickChart from '../charts/CandlestickChart';

// Sample data for the list
const dataListD = [
  { id: 1, name: 'Item 1', value: 100 },
  { id: 2, name: 'Item 2', value: 200 },
  { id: 3, name: 'Item 3', value: 300 },
];

let dateF = "";
const chartData = [];
/* eslint react/prop-types: 0 */
export default function TickerPortfolio({ symbol, date, principal }) {
  const [dataList, setDataList] = useState([]);

  useEffect(() => {
    async function getTickerPortfolio() {
      const url = 'http://127.0.0.1:5000/gettickport';
      const myHeaders = new Headers();
      myHeaders.append("Content-Type", "application/json");
      const response = await fetch(url, {
        method: 'POST',
        headers: myHeaders,
        body: JSON.stringify({ symbol, date, principal}),
      });
      const data = await response.json();
      setDataList(data);
      
      dateF = data.date;

      const dailyData = data.daily_data_cache;
      Object.keys(dailyData).forEach((key) => {
        chartData.push({
          x: new Date(dailyData[key].x),
          y: dailyData[key].y.slice(0, 4),
        });
      });
      // console.log(chartData);
      window.dispatchEvent(new Event('resize'))
    }
    getTickerPortfolio();
  }, [symbol, date, principal]);
  console.log(dataList);

  return (
    <Card>
      <Grid container spacing={0}>
        <Grid item xs={12} sm={12} md={12} p={2}>
          <Typography variant="h4" sx={{ mb: 5 }}>
            Symbol: {symbol} \ Date: {dateF} \ Principal: ${principal}
          </Typography>
        </Grid>
        <Grid item xs={12} sm={2} md={2} p={1}>
          <List>
            {dataListD.map((item) => (
              <ListItem key={item.id}>
                <ListItemText primary={item.name} secondary={`Value: ${item.value}`} />
              </ListItem>
            ))}
          </List>
        </Grid>
        <Grid item xs={12} sm={10} md={10} p={1}>
          <Box><CandlestickChart data={chartData} /></Box>
        </Grid>
      </Grid>
    </Card>
  );
}
