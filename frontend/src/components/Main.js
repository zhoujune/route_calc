import * as React from "react";
import Typography from "@material-ui/core/Typography";
import Grid from "@material-ui/core/Grid";
import TextField from "@material-ui/core/TextField";
import Box from "@material-ui/core/Box";
import Button from "@material-ui/core/Button";
import Popover from "@material-ui/core/Popover";
import Select from "@material-ui/core/Select";
import MenuItem from "@material-ui/core/MenuItem";
import Snackbar from "@material-ui/core/Snackbar";

export default function MainForm() {
  const [edit, setEdit] = React.useState(false);
  const [newroute, setNewroute] = React.useState(false);
  const [routes, setRoutes] = React.useState([]);
  const [curroute, setCurroute] = React.useState(1);
  const [curcode, setCurcode] = React.useState("");
  const [msgOpen, setMsgOpen] = React.useState(false);
  const [msg, setMsg] = React.useState("");
  const [addrs, setAddrs] = React.useState("");

  const [routeName, setRouteName] = React.useState("");
  const [routeInfo, setRouteInfo] = React.useState("");
  const [mapURL, setMapURL] = React.useState("");
  const [mapDist, setMapDist] = React.useState(999999);
  const [mapTime, setMapTime] = React.useState("");
  const [seeMap, setSetMap] = React.useState(false);

  React.useEffect(() => {
    let isActive = true;
    fetch("route/allRoutes")
      .then((response) => response.json())
      .then((data) => {
        if (isActive) {
          setRoutes(data);
        }
      })
      .catch((error) => console.log(error.message));

    return () => {
      isActive = false;
    };
  });

  const handleClick = () => {
    if (edit) {
      setEdit(false);
    } else {
      setEdit(true);
    }
  };

  const handleClose = () => {
    setInfo_open(false);
  };

  const handleEdit = () => {
    if (edit) {
      setEdit(false);
    } else {
      setEdit(true);
      setNewroute(false);
    }
  };

  const showMsg = (flag) => {
    if (flag) {
      setMsg("Success!");
      setMsgOpen(true);
    } else {
      setMsg("Failed!");
      setMsgOpen(true);
    }
  };

  const handleAddingSubmit = () => {
    const requestOptions = {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        code: routeName,
        addrs: routeInfo,
      }),
    };
    fetch("/route/createRoute", requestOptions)
      .then((response) => response.json())
      .then((data) => {
        showMsg(true);
      })
      .catch((error) => showMsg(false));
  };

  const handleEditSubmit = () => {
    const requestOptions = {
      method: "PATCH",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        id: curroute,
        code: curcode,
        addrs: addrs,
      }),
    };
    fetch("/route/updateRoute", requestOptions)
      .then((response) => response.json())
      .then((data) => {
        showMsg(true);
        setMapURL(data.image_url);
        setMapDist(data.total_dist);
        setMapTime(data.total_time)
      })
      .catch((error) => showMsg(false));
  };

  const handleNew = () => {
    if (newroute) {
      setNewroute(false);
    } else {
      setNewroute(true);
      setEdit(false);
    }
  };

  const renderAdding = () => {
    return (
      <div>
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
              onChange={(ev) => setRouteName(ev.target.value)}
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
              onChange={(ev) => setRouteInfo(ev.target.value)}
            />
          </Grid>
          <Grid item xs={12} md={12}>
            <Box textAlign="center">
              <Button
                onClick={handleAddingSubmit}
                variant="contained"
                sx={{ mt: 3, ml: 1 }}
              >
                Submit
              </Button>
            </Box>
          </Grid>
        </Grid>
      </div>
    );
  };

  const renderEditing = () => {
    return (
      <div>
        <Typography variant="h6" gutterBottom>
          Editing Route
        </Typography>
        <Grid container spacing={3}>
          <Grid item xs={12} md={6}>
            <TextField
              required
              id="route name"
              label="Route name"
              fullWidth
              variant="standard"
              value={curcode}
              onChange={(ev) => setCurcode(ev.target.value)}
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
              value={addrs}
              onChange={(ev) => setAddrs(ev.target.value)}
            />
          </Grid>
          <Grid item xs={12} md={12}>
            <Box textAlign="center">
              <Button
                onClick={handleEditSubmit}
                variant="contained"
                sx={{ mt: 3, ml: 1 }}
              >
                Submit
              </Button>
            </Box>
          </Grid>
        </Grid>
      </div>
    );
  };

  return (
    <React.Fragment>
      <Typography variant="h6" gutterBottom>
        Sign up for a route
      </Typography>
      <Snackbar
        open={msgOpen}
        autoHideDuration={1000}
        onClose={() => setMsgOpen(false)}
        message={msg}
      />
      <Grid container spacing={3}>
        <Grid item xs={12} md={6}>
          <Select
            fullWidth
            labelId="route_select"
            id="route_select"
            value={curroute || 1}
            label="Find Routes"
            onChange={(ev) => {
              setCurroute(ev.target.value);
            }}
          >
            {routes.map((route) => (
              <MenuItem
                value={route.id}
                code={route.code}
                onClick={() => {
                  setCurcode(route.code);
                  setAddrs(route.addrs);
                  setMapURL(route.image_url);
                  setMapDist(route.total_dist);
                  setMapTime(route.total_time);
                  setSetMap(false)
                }}
              >
                <li>{route.code}</li>
              </MenuItem>
            ))}
          </Select>
        </Grid>
        <Grid item xs={12} md={6}>
          <Box textAlign="center">
            <Button
              onClick={handleEdit}
              variant="contained"
              sx={{ mt: 3, ml: 1 }}
            >
              Edit route
            </Button>

            <Popover
              open={edit}
              onClose={handleEdit}
              anchorOrigin={{
                vertical: "bottom",
                horizontal: "left",
              }}
            >
              {renderEditing()}
            </Popover>

            <Button
              onClick={handleNew}
              variant="contained"
              sx={{ mt: 3, ml: 1 }}
            >
              New Route
            </Button>

            <Popover
              open={newroute}
              onClose={handleNew}
              anchorOrigin={{
                vertical: "bottom",
                horizontal: "left",
              }}
            >
              {renderAdding()}
            </Popover>
          </Box>
        </Grid>

        <Grid item xs={12} md={12}>
          <Box textAlign="center">
            <Button
              onClick={() => setSetMap(true)}
              variant="contained"
              sx={{ mt: 3, ml: 1 }}
            >
              SignUp
            </Button>
          </Box>
        </Grid>
        { seeMap ?
        <Grid item xs={12} md={12}>
            <img
              src={mapURL}
            />
            <figcaption>Distance: {mapDist} meters; Time: {mapTime}</figcaption>
          </Grid> : <div/>}

      </Grid>
    </React.Fragment>
  );
}
