import { useMemo, useState, useEffect } from 'react';

import Stack from '@mui/material/Stack';
import Container from '@mui/material/Container';
import Grid from '@mui/material/Unstable_Grid2';
import Typography from '@mui/material/Typography';

import ProductFilters from '../product-filters';

// ----------------------------------------------------------------------

export default function ProductsView() {
  const [openFilter, setOpenFilter] = useState(false);
  const [filteredData, setFilteredData] = useState([]); // State for storing filtered data
  
  const defaultOptions = useMemo(() => ({
    option1: 'Accessories',
    option2: 'All',
    option3: 'All',
    option4: 'All',
    option5: 'Accessories',
  }), []);

  useEffect(() => {
    // Fetch data with default filter options when the component mounts    
    fetchFilteredData(defaultOptions);
  }, [defaultOptions]);
  

  const handleOpenFilter = () => {
    setOpenFilter(true);
  };

  const handleCloseFilter = () => {
    setOpenFilter(false);
  };

  const fetchFilteredData = async (filterOptions) => {
    // try {
      // Example API call using axios, replace with your actual API endpoint
      // const response = await axios.post('/api/getFilteredData', {
        // filters: filterOptions,
      // });

      // setFilteredData(response.data);
    // } catch (error) {
      // console.error('Failed to fetch filtered data', error);
    // }
  };

  const handleSave = (savedSelections) => {
    console.log(savedSelections);

    // Trigger API call with selected filters
    fetchFilteredData(savedSelections);

    handleCloseFilter();
  };

  return (
    <Container>
      <Stack direction="row" alignItems="center" justifyContent="space-between" sx={{ mb: 5 }}>
        <Typography variant="h4">Screen Tickers</Typography>

        <Stack direction="row" spacing={1}>
          <ProductFilters
            openFilter={openFilter}
            onOpenFilter={handleOpenFilter}
            onCloseFilter={handleCloseFilter}
            onSave={handleSave}
            defaultOptions={defaultOptions}
          />
        </Stack>
      </Stack>

      <Grid container spacing={3}>
        {/* Render the filtered data here */}
        {filteredData.map((item, index) => (
          <Grid key={index} xs={12} sm={6} md={3}>
            {/* <Typography variant="body1">{item.name}</Typography> */}
          </Grid>
        ))}
      </Grid>
    </Container>
  );
}
