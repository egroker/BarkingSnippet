# BarkingSnippet

Here are some examples of my VFX experience.

Below is presented information about each code piece.

# AutoFX Snippet

This code is a bit pointless without whole pipeline infrustructure, which I
obviously cannot include here, but it shows some directions of my usage of
houdini api, django and templates.

Bead class represents Job on farm or local machine.

# Katana Project Livegroup

I've been adding quality switcher and attributes extraction to this livegroup.
Project livegroup is presented in each katana shot file and is used across whole project.

# Render Calculator

Simple data analysis tool, used for presenting information from our Clickhouse Database. which contains render statistics.
It is jupyter notebook file, which is distributed to local network via voila service.

# Texture Converter

Qt window, used by artists separately from pipeline if they need anything converted.
Usually during texture publish, pipeline does all convertions automatically, but sometimes
they need to convert HDRs, out-of-pipe textures and etc.