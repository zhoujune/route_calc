import * as React from 'react';
import Typography from "@material-ui/core/Typography";
import Grid from "@material-ui/core/Grid";
import TextField from "@material-ui/core/TextField";
import Box  from "@material-ui/core/Box";
import Button  from "@material-ui/core/Button";
import Checkbox from "@material-ui/core/Checkbox";

/*
Jun Zhou
2022/4/6
NO right truly reserved
*/

export default function PaymentForm() {


  const handleSubmit = () => {
        
      };
  return (
    <React.Fragment>
      <Typography variant="h6" gutterBottom>
        Add Route
      </Typography>
      <Grid container spacing={3}>
        <Grid item xs={12} md={6}>
          <TextField
            required
            id="route name"
            label="Route name"
            fullWidth
            variant="standard"
          />
        </Grid>
        <Grid item xs={12} md={6}>
          <TextField
            id="route info"
            label="route info"
            fullWidth
            variant="standard"
          />
        </Grid>
        <Grid item xs={12} md={12}>
        <TextField
          required
          id="outlined-multiline-static"
          label="Cities info"
          multiline
          rows={4}
          fullWidth
          variant="outlined"
        />
        </Grid>
        <Grid item xs={12} md={12}>
        <Box textAlign='center'>
        <Button onClick={handleSubmit} variant="contained" sx={{ mt: 3, ml: 1 }}>
                      Submit
        </Button>
        </Box>
        </Grid>
      </Grid>
    </React.Fragment>
  );
}