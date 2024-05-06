using GLMakie

# GLMakie.activate!()
# scene = Scene(backgroundcolor=:black)
# subwindow = Scene(scene, viewport=Rect(100, 100, 200, 200), clear=true, backgroundcolor=:tomato)
# scene

# cam3d!(subwindow)
# meshscatter!(subwindow, rand(Point3f, 10), color=:tomato)
# center!(subwindow)
# scene

# subwindow.clear = false
# relative_space = Makie.camrelative(subwindow)
# # this draws a line at the scene window boundary
# lines!(relative_space, Rect(0, 0, 1, 1))
# scene

# campixel!(scene)
# w, h = size(scene) # get the size of the scene in pixels
# # this draws a line at the scene window boundary
# image!(scene, [sin(i/w) + cos(j/h) for i in 1:w, j in 1:h])
# scene

# translate!(scene.plots[1], 0, 0, -10000)
# scene

# screen = display(scene) # use display, to get a reference to the screen object
# depth_color = GLMakie.depthbuffer(screen)
# close(screen)
# # Look at result:
# f, ax, pl = heatmap(depth_color)
# Colorbar(f[1, 2], pl)
# f

# on(scene.events.mouseposition) do mousepos
#   if ispressed(subwindow, Mouse.left & Keyboard.left_control)
#       subwindow.viewport[] = Rect(Int.(mousepos)..., 200, 200)
#   end
# end

scene = Scene(backgroundcolor=:gray)
lines!(scene, Rect2f(-1, -1, 2, 2), linewidth=5, color=:black)
scene

cam = Makie.camera(scene)

cam.projection[] = Makie.orthographicprojection(-3f0, 5f0, -3f0, 5f0, -100f0, 100f0)
scene

w, h = size(scene)
nearplane = 0.1f0
farplane = 100f0
aspect = Float32(w / h)
cam.projection[] = Makie.perspectiveprojection(45f0, aspect, nearplane, farplane)
# Now, we also need to change the view matrix
# to "put" the camera into some place.
eyeposition = Vec3f(10)
lookat = Vec3f(0)
upvector = Vec3f(0, 0, 1)
cam.view[] = Makie.lookat(eyeposition, lookat, upvector)
scene