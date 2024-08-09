// src/components/TickerPortfolio.js
import React from 'react';

import { Box, List, Card, Grid, ListItem, Typography, ListItemText } from '@mui/material';

import CandlestickChart from '../charts/CandlestickChart';

// Sample data for the list
const dataList = [
  { id: 1, name: 'Item 1', value: 100 },
  { id: 2, name: 'Item 2', value: 200 },
  { id: 3, name: 'Item 3', value: 300 },
];

/* eslint react/prop-types: 0 */
export default function TickerPortfolio({ symbol, date, principal }) {
  async function getTickerPortfolio() {
    const url = 'http://127.0.0.1:5000/test/';
    const response = await fetch(url);
    const data = await response.json();
    return data;
  }
  // console.log(JSON.parse(getTickerData()));
  getTickerPortfolio()
  .then(result => console.log(result));
  return (
    <Card>
      <Grid container spacing={0}>
        <Grid item xs={12} sm={12} md={12} p={2}>
          <Typography variant="h4" sx={{ mb: 5 }}>
            {symbol} \ {date} \ Principal: ${principal}
          </Typography>
        </Grid>
        <Grid item xs={12} sm={2} md={2} p={1}>
          <List>
            {dataList.map((item) => (
              <ListItem key={item.id}>
                <ListItemText primary={item.name} secondary={`Value: ${item.value}`} />
              </ListItem>
            ))}
          </List>
        </Grid>
        <Grid item xs={12} sm={10} md={10} p={1}>
          <Box><CandlestickChart /></Box>
        </Grid>
      </Grid>
    </Card>
  );
}
