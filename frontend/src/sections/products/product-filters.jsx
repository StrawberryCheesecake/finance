import PropTypes from 'prop-types';
import React, { useState } from 'react';

import Box from '@mui/material/Box';
import Stack from '@mui/material/Stack';
import Radio from '@mui/material/Radio';
import Button from '@mui/material/Button';
import Drawer from '@mui/material/Drawer';
import Divider from '@mui/material/Divider';
import RadioGroup from '@mui/material/RadioGroup';
import Typography from '@mui/material/Typography';
import IconButton from '@mui/material/IconButton';
import FormControlLabel from '@mui/material/FormControlLabel';

import Iconify from 'src/components/iconify';
import Scrollbar from 'src/components/scrollbar';

export const SCREENER_OPTIONS = {
  option1: ['All', 'Shoes', 'Apparel', 'Accessories'],
  option2: ['All', 'Shoes', 'Apparel', 'Accessories'],
  option3: ['All', 'Shoes', 'Apparel', 'Accessories'],
  option4: ['All', 'Shoes', 'Apparel', 'Accessories'],
  option5: ['All', 'Shoes', 'Apparel', 'Accessories'],
};

export default function ProductFilters({ openFilter, onOpenFilter, onCloseFilter, onSave, defaultOptions }) {
  // State to manage selected options
  const [selections, setSelections] = useState(defaultOptions);

  // Handler to update selection
  const handleSelectionChange = (event, optionKey) => {
    setSelections({
      ...selections,
      [optionKey]: event.target.value,
    });
  };

  // Reset handler
  const handleReset = () => {
    setSelections(defaultOptions);
  };

  // Save handler
  const handleSave = () => {
    onSave(selections);
    onCloseFilter();
  };

  // Render screener categories
  const renderCategory = (optionKey) => (
    <Stack spacing={1} key={optionKey}>
      <Typography variant="subtitle2">Category {optionKey}</Typography>
      <RadioGroup
        value={selections[optionKey]}
        onChange={(event) => handleSelectionChange(event, optionKey)}
      >
        {SCREENER_OPTIONS[optionKey].map((item) => (
          <FormControlLabel key={item} value={item} control={<Radio />} label={item} />
        ))}
      </RadioGroup>
    </Stack>
  );

  return (
    <>
      <Button
        disableRipple
        color="inherit"
        endIcon={<Iconify icon="ic:round-filter-list" />}
        onClick={onOpenFilter}
      >
        Select Screener Filters&nbsp;
      </Button>

      <Drawer
        anchor="right"
        open={openFilter}
        onClose={onCloseFilter}
        PaperProps={{
          sx: { width: 280, border: 'none', overflow: 'hidden' },
        }}
      >
        <Stack
          direction="row"
          alignItems="center"
          justifyContent="space-between"
          sx={{ px: 1, py: 2 }}
        >
          <Typography variant="h6" sx={{ ml: 1 }}>
            Filters
          </Typography>
          <IconButton onClick={onCloseFilter}>
            <Iconify icon="eva:close-fill" />
          </IconButton>
        </Stack>

        <Divider />

        <Scrollbar>
          <Stack spacing={3} sx={{ p: 3 }}>
            {Object.keys(SCREENER_OPTIONS).map((optionKey) => renderCategory(optionKey))}
          </Stack>
        </Scrollbar>

        <Box sx={{ p: 3 }}>
          <Button
            fullWidth
            size="large"
            type="button"
            color="inherit"
            variant="outlined"
            startIcon={<Iconify icon="ic:round-clear-all" />}
            onClick={handleReset}
          >
            Reset to Default
          </Button>
          <Button
            fullWidth
            size="large"
            type="button"
            color="primary"
            variant="contained"
            sx={{ mt: 2 }}
            onClick={handleSave}
          >
            Save & Show
          </Button>
        </Box>
      </Drawer>
    </>
  );
}

ProductFilters.propTypes = {
  openFilter: PropTypes.bool,
  onOpenFilter: PropTypes.func,
  onCloseFilter: PropTypes.func,
  onSave: PropTypes.func.isRequired,
};
