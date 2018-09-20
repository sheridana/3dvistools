Blender addon for 3d visualization of segmented data (or any other mesh object) - still working on integrating curve functionality to all operators  

Inspiration from https://github.com/schlegelp/CATMAID-to-Blender  

Current operators:
  * Batch import
    * Allows you to import .obj or .raw files from file
    * Can choose os
    * Can decimate on import (memory constraint for folders containing a lot of large objects - will import, decimate apply, for every object in folder - but is slower than non memory constraint)
    * Figure out image plane import
    
  * New window
    * Allows you to duplicate a chosen window type (text editor,3d view, timeline, etc) into a new window
    * Need to add remove scene function because for whatever reason, this creates a new scene that we don't need
  
  * View mode
    * Allows you to change multiple view properties at once
    * Object interaction mode
    * Display method
    * Persp/ortho, can define which direction
    * Toggle quad view, lock, box, clip
    * Figure out polling problem when in quad view and trying to change persp/ortho
  
  * World background
    * Allows you to change world background (paper sky, blend, real sky)
    * Add transparent background option
  
  * Modifiers
    * Allows you to add, edit, remove, link, apply modifiers
    * Currently only have decimation working, need to add other modifiers to it
  
  * Jump fix
    * This operator is generally intended for fixing artifacts on imported catmaid skeletons if there are a lot in some concentrated location (i.e central complex neurons)
    * Can remove spline points (curve objects) within a given range on a given axis (i.e wedge and tile neurons have a large z axis jump between -24 and -21)
    * Can convert objects to mesh and intersect jump points with a defined cube mesh to remove them
  
  * Bounding box
    * Create single or individual bounding boxes around selected objects' combined or indivual max and min coords
    * For single box, currently duplicates selected objects, joins, creates mesh, sets mesh properties to joined object, deletes joined object
    * Change this to input selected objects max and min axis dimensions to array, then set cube dimensions to max and min of array
    * Also currently finnicky if multiple other cubes already in scene, fix this too
  
  * Object manipulation
    * Allows you to edit object scale, location, rotation, origin, pivot point, and whether you want to smooth them
    * Also lets you define which objects you want to edit (selected, all, or by name) 
    * If using by name, you can select partial match, which ignores case, commas, etc.  Can also use is not named to edit all things not named some string - can use with partial match too
    * Have to fix the is not method so that it only targets current layer objects, rather than all scene objects
    * Also need to create a separate object list class and call it whenever it's needed because multiple operators use this, and it should be added to other operators too
  
  * Materials
    * This is very similar to the change materials function in CATMAID-to-Blender with a couple changes
    * Lets you give objects materials, change single color, diffuse/specular intensity, emit, material type, transparency, random colors
  
  * Color map
    * Gives selected objects a heat map gradient based on vertex count or surface area
    * Can use on meshes or curves (if surface area, needs to be mesh)
    * Can do hue range, emit range, alpha/specular/fresnel range
    * Can define low to high (large objects highlighted) or high to low (small objects highlighted)
    * Can define range for each
    * Need to define whether it uses transparency or not, currently once alpha/specular/fresnel are selected, can only not use transparency if all are unselected
  
  * Edit objects
    * Need to add executable stuff to this
    * This will actually be super useful because in blender you can only edit one object at a time
    * Things to add: bevel depth, vertex dilation/erosion, vertex/edge/face mode, sort elements by cursor distance, flip normals, remove doubles, convert tris to quads/vice versa
  
  * Batch export
    * Need to add executable stuff to this
    * Export obj, raw, json (threejs json loader format), figure out image planes
    * Figure out file directory structure rather than absolute path
  
  * Peel away
    * Give selected objects (i.e image planes) an axis offset - basically defined spacing between objects
    * i.e if you have fafb stack images, give them spacing between sections on z axis to give 3d-ness to plane stack
    * Create simple peel away by automatically adding visibility keyframes (by default, all visible at start, one plane or object becomes invisible at each subsequent frame), more options available in animation operator
  
  * Animation
    * Create an animation for selected objects
    * Object animations: expand (need to make this - objects will scale around a center point), visibility (fade in/hold/fade out with visibility keyframes), materials (fade in/hold/fade out with transparency keyframes)
    * Static camera stuff: add camera, snap to selected/view (with optional padding), perspective vs ortho (neeed to make all these)
    * Camera animations: zoom, move (make these)
    * Static empty stuff: add empty, snap to center of selected objects (need to make this)
    * Empty animation: rotation, (need to make this)
    * Render image with ouput file option (make this)
    * Render video with ouput file option (make this)
  
  
  * Automate
    * Single operator to do aforementioned stuff at once (needs work)
 
Todos:

  * Add info tabs to all operators with more detailed descriptions
  * Create wiki tutorial with images/videos and examples
  
  * Dupliverts
  * Grouping & parenting
  
  * Object statistics (cable length, surface area, vertex count etc) (write to csv?)
  
  * Multiple materials to objects based on some criteria (say boutons vs dendrites etc)
  
  * Exportable meta tags
