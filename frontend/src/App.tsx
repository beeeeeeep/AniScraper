import React, {useState} from 'react';
import logo from './logo.svg';
import './App.css';
import {AppBar, CssBaseline, Drawer, IconButton, makeStyles, Toolbar} from "@material-ui/core";
import clsx from "clsx";
import MenuIcon from "@material-ui/icons/Menu";

const drawerWidth = 240;

const useStyles = makeStyles((theme) => ({
    root: {
        display: "flex",
    },
    appBar: {
        zIndex: theme.zIndex.drawer + 1,
        transition: theme.transitions.create(["width", "margin"], {
            easing: theme.transitions.easing.sharp,
            duration: theme.transitions.duration.leavingScreen,
        }),
    },
    appBarShift: {
        marginLeft: drawerWidth,
        width: `calc(100% - ${drawerWidth}px)`,
    },
    toolbar: {
        paddingRight: 24,
    },
    menuButton: {
        marginRight: 26,
    },
    drawerPaper: {
        position: 'relative',
        whiteSpace: 'nowrap',
        width: drawerWidth,
        transition: theme.transitions.create('width', {
            easing: theme.transitions.easing.sharp,
            duration: theme.transitions.duration.enteringScreen,
        }),
    },
    drawerPaperClose: {
        overflowX: 'hidden',
        transition: theme.transitions.create('width', {
            easing: theme.transitions.easing.sharp,
            duration: theme.transitions.duration.leavingScreen,
        }),
        width: theme.spacing(7),
        [theme.breakpoints.up('sm')]: {
            width: theme.spacing(9),
        },
    },
    content: {
        flexGrow: 1,
        height: "100vh",
        overflow: "auto",
    },
    appBarSpacer: theme.mixins.toolbar,
}));

function App() {
    const classes = useStyles();
    const [appBarOpen, setAppBarOpen] = useState<boolean>(true);

    return (
        <div className={classes.root}>
            <CssBaseline />
            <AppBar position="absolute" className={clsx(classes.appBar, appBarOpen && classes.appBarShift)}>
                <Toolbar className={classes.toolbar}>
                    <IconButton
                        edge="start"
                        color="inherit"
                        aria-label="open drawer"
                        onClick={() => setAppBarOpen(!appBarOpen)}
                        className={clsx(classes.menuButton)}
                    >
                        <MenuIcon />
                    </IconButton>
                </Toolbar>
            </AppBar>
            <Drawer
                variant="permanent"
                classes={{
                    paper: clsx(classes.drawerPaper, !appBarOpen && classes.drawerPaperClose),
                }}
                open={appBarOpen}
            >
                Drawer stuff
            </Drawer>
            <main className={classes.content}>
                <div className={classes.appBarSpacer} />
            </main>
        </div>
    );
}

export default App;
