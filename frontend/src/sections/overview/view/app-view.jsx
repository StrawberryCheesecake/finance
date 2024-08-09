import Container from '@mui/material/Container';
import Grid from '@mui/material/Unstable_Grid2';
import Typography from '@mui/material/Typography';

import TickerPortfolio from 'src/homebrew/portfolios/TickerPortfolio';

// ----------------------------------------------------------------------

export default function AppView() {
  return (
    <Container maxWidth="xl">
      <Grid>
      <Typography variant="h4" sx={{ mb: 5 }}>
        Ticker Portfolios
      </Typography>

        <Grid xs={12} md={6} lg={8}>
          <TickerPortfolio symbol="APPL" date="today" principal={10000}/>
        </Grid>
      </Grid>
    </Container>
  );
}
