package main

import (
	"log"
	"net/http"

	"github.com/labstack/echo/v5"
	"github.com/pocketbase/pocketbase"
	"github.com/pocketbase/pocketbase/apis"
	"github.com/pocketbase/pocketbase/core"
)

var homeView = echo.Route{
	Method: http.MethodGet,
	Path:   "/",
	Handler: func(c echo.Context) error {
		return c.String(200, "Why, Hello there!")
	},
}

func beforeServe(e *core.ServeEvent) error {
	// serves static files from the provided public dir (if exists)
	subFs := echo.MustSubFS(e.Router.Filesystem, "pb_public")
	e.Router.GET("/*", apis.StaticDirectoryHandler(subFs, false))

	e.Router.AddRoute(homeView)

	return nil
}

func main() {
	app := pocketbase.New()

	app.OnBeforeServe().Add(beforeServe)

	if err := app.Start(); err != nil {
		log.Fatal(err)
	}
}
