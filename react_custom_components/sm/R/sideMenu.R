# AUTO GENERATED FILE - DO NOT EDIT

sideMenu <- function(id=NULL, items=NULL, className=NULL) {
    
    props <- list(id=id, items=items, className=className)
    if (length(props) > 0) {
        props <- props[!vapply(props, is.null, logical(1))]
    }
    component <- list(
        props = props,
        type = 'SideMenu',
        namespace = 'sm',
        propNames = c('id', 'items', 'className'),
        package = 'sm'
        )

    structure(component, class = c('dash_component', 'list'))
}
