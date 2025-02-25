from yak.djangles import KomponentMapper


map_component = KomponentMapper(map_to='calico')
mapper = {
    **{tag: tag for tag in ('slot', 'slotvalue')},
    'component': map_component
}
