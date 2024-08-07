// src/components/TickerPortfolio.js
import React from 'react';
import { Box, Typography, List, ListItem, ListItemText } from '@mui/material';
import CandlestickChart from '../charts/CandlestickChart';

// Sample data for the list
const dataList = [
  { id: 1, name: 'Item 1', value: 100 },
  { id: 2, name: 'Item 2', value: 200 },
  { id: 3, name: 'Item 3', value: 300 },
];

function TickerPortfolio() {
  return (
    <Box
      sx={{
        display: 'flex',
        flexDirection: 'row',
        alignItems: 'center',
        justifyContent: 'center',
        gap: 4,
        p: 2,
      }}
    >
      {/* Title and List Section */}
      <Box sx={{ flex: 1 }}>
        <Typography variant="h4" gutterBottom>
          My Data List
        </Typography>
        <List>
          {dataList.map((item) => (
            <ListItem key={item.id}>
              <ListItemText
                primary={item.name}
                secondary={`Value: ${item.value}`}
              />
            </ListItem>
          ))}
        </List>
      </Box>

      {/* Graph Section */}
      <Box sx={{ flex: 2 }}>
        <CandlestickChart />
      </Box>
    </Box>
  );
}

export default TickerPortfolio;