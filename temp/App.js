import React from "react";
import ReactDOM from "react-dom/client";
import TickerPortfolio from "./portfolios/TickerPortfolio";
import App from "./App";
import { CssBaseline, ThemeProvider, createTheme } from "@mui/material";

const theme = createTheme();

const root = ReactDOM.createRoot(document.getElementById("root"));
root.render(
  <ThemeProvider theme={theme}>
    <CssBaseline />
    <TickerPortfolio />
    <TickerPortfolio />
  </ThemeProvider>
);

export default App;