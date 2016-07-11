import bpy
import bmesh
import random
from random import uniform
from mathutils import Vector

class RandomSpheres():
    
         
    def __init__(self, domain=1,scale = [1,1],initial_count=200):
        
        self.count = initial_count
        self.spheres = []
        self.context = bpy.context
        self.scale= scale
        self.domain = domain
        ## set to Object mode and delete all the previous Spheres
        try:
            bpy.ops.object.mode_set(mode='OBJECT')
        except RuntimeError:
            print("OBJECT mode is already selected!")

        self.scene = bpy.context.scene

        for ob in self.scene.objects:
            if ob.type == 'MESH':
                ob.select = True
            else: 
                ob.select = False
        bpy.ops.object.delete()
        
        #Add material if doesnt exist
        mat = bpy.data.materials.get("randobjcol")
        if not mat:
            mat = bpy.data.materials.new("randobjcol")
            mat.use_object_color = True
        self.mat=mat  
        #Creat bounding box if it doesnt exist
        boundbox = bpy.data.objects.get("BoundBOX")
        if not boundbox:
            bpy.ops.mesh.primitive_cube_add()
            boundbox = context.scene.objects.active
            boundbox.name = "BoundBOX"
            boundbox.draw_type = 'WIRE'
            boundbox.hide_select = True
            boundbox.location = (0, 0, 0)

        if not self.scene.objects.get("BoundBOX"):
            self.scene.objects.link(boundbox)
        #Scale the Bounding box to the assigned domain size
        boundbox.scale = self.domain * Vector((1, 1, 1))
        
    def random_sphere(self,sphere,only_spheres=False):
        
        # random scale and rotation for sphere based on settings
        if only_spheres:
            scale = uniform(self.scale[0] , self.scale[1]) * Vector((1, 1, 1))
        else:
            scale = Vector([uniform(self.scale[0], self.scale[1]) for c in "xyz"])
        scale = Vector([min(s, self.domain) for s in scale])
        dom = self.domain - max(scale) 
        sphere.scale = scale
        sphere.location = Vector([uniform(-dom, dom) for c in "xyz"])  
          
    def PopulateDomain(self, use_context_object = False,only_spheres = False):
        
        #populate the bounding box with spheres 
        self.spheres = []
        obj = self.context.object
        if use_context_object and obj:
            sphere = obj
        else:
            bpy.ops.mesh.primitive_uv_sphere_add()
            sphere = self.context.scene.objects.active
            bpy.ops.object.shade_smooth()
            self.scene.objects.unlink(sphere)

            sphere.active_material = self.mat

        for i in range(self.count):
            self.spheres.append(sphere)
            self.random_sphere(sphere,only_spheres)    
            sphere = sphere.copy()
            #self.context.scene.objects.link(sphere)  

    def within_touch(self,s1, s2):
        
        #Check if the spheres are touching, if yes returns a vector to move away
        def r(s):
            return max(s.scale)

        d = (s2.location - s1.location)
        r1, r2 = r(s1), r(s2)
        radsum = r(s1) + r(s2)
        if d.length <= 0.0001:
            return Vector((r1, r1, r1))
            # same position    
        elif d.length < radsum:
            # return a vector to move away
            d.length = radsum - d.length
            return  -d
        return Vector()

    def checkbounds(self,sphere, fix):
        
        loc = sphere.location + fix
        dm = max(sphere.scale)
        _min = -self.domain + dm
        _max =  self.domain - dm
        for i, v in enumerate(loc):
            if v < _min:
                loc[i] = _min
            if v > _max:
                loc[i] = _max
        return loc


    def SphereAdjust(self,tries_per_sphere =250):
        
        
        tries = 0
        t_count = 0
        r_count = 0
        fix = Vector()
        sphere = self.spheres.pop()
        arranged_spheres = [sphere]
        sphere = self.spheres.pop()

        while sphere and tries < tries_per_sphere * self.count:
            if t_count > 5 and abs(self.scale[0] - self.scale[1]) > 0.00001:
                sphere.scale = Vector([max(s, self.scale[0]) for s in sphere.scale])        
            touchers = [s for s in [self.within_touch(sphere, s) for s in arranged_spheres] if s.length > 0]
            if len(touchers):
                fix = Vector()
                for v in touchers:
                    fix += v
                if (fix < 0.0001) or r_count > tries_per_sphere / 2:
                    r_count = 0
                    self.random_sphere(sphere)          
                else:
                    loc = self.checkbounds(sphere, fix)
                    sphere.location = loc
                    t_count += 1
                    r_count += 1
                    tries += 1
            else:
                t_count = 0
                r_count = 0
                arranged_spheres.append(sphere)
                sphere =  self.spheres.pop() if len(self.spheres) else None

        for s in arranged_spheres:
            if not self.scene.objects.get(s.name):
                self.scene.objects.link(s)
        
        self.spheres = arranged_spheres


    def returnSpheres(self):
        return self.spheres
    
    def VolumeFraction(self):
        
        
        def get_vol_tri(tri):  
            p0 = tri[0]
            p1 = tri[1]
            p2 = tri[2]
            vcross = cross_product(p1,p2)
            vdot = dot_product(p0, vcross)
            vol = vdot/6
            return vol


        def cross_product(v0, v1):
            x =   v0[1]*v1[2] - v0[2]*v1[1]
            y = -(v0[0]*v1[2] - v0[2]*v1[0])
            z =   v0[0]*v1[1] - v0[1]*v1[0]
            return [x,y,z]


        def dot_product(v0,v1):
            vec = [v0[n]*v1[n] for n in range(len(v0))]
            return sum(vec)

        def fget_vol(ob):
            obj = ob.data
            if hasattr(obj, 'polygons'):
            # if mesh not closed, don't calculate volume
                if ob.is_open:
                    return 'open mesh has no volume'
                else:
                    n_faces = len(obj.polygons)
                    vol = 0
                    for f in range(0, n_faces):
                        n_vertices = len(obj.polygons[f].vertices[:])
                        if n_vertices != 3:  # faces must be triangles
                            for v in range(0, n_vertices):
                                return 'highlight a subregion'
                        tri = [0] * n_vertices
                        for v in range(0, n_vertices):
                            tri[v] = obj.vertices[obj.polygons[f].vertices[v]].co
                        vol += get_vol_tri(tri)
                    return vol
            else:
                return 'property not available'


        def triangulate_object(obj):
            mesh = obj.data
            # Get a BMesh representation
            bm = bmesh.new()
            bm.from_mesh(mesh)

            bmesh.ops.triangulate(bm, faces=bm.faces[:], quad_method=0, ngon_method=0)

            # Finish up, write the bmesh back to the mesh
            bm.to_mesh(mesh)
            bm.free()
            
        vol=0.0
        for ob in self.scene.objects:
            if ob.type == 'MESH' and ob.name.startswith("Sphere"):
                ob.select = True
                triangulate_object(ob)
                vol+=fget_vol(ob)*ob.scale[0]*ob.scale[1]*ob.scale[2]
        
        
        return vol/(2*self.domain)**3


class CamLight():
    
    def __init__(self,type,domain):
        
        def look_at(obj, point, loc):
            
            for ob in obj:
                ob.location = loc
                direction = point - loc
                rot_quat = direction.to_track_quat('-Z', 'Y')
                ob.rotation_euler = rot_quat.to_euler()
                
        if type=="3D":
            loc = Vector([domain*4,domain*4,domain*4])
            obj_camera = bpy.data.objects["Camera"]
            obj_light = bpy.data.objects["Lamp"]
            obj_camera.data.type = "PERSP"
            obj_other = bpy.data.objects["BoundBOX"]
            look_at([obj_camera,obj_light],obj_other.location,loc)
        elif type=="2D":
            loc = Vector([0,0,domain*5])
            obj_camera = bpy.data.objects["Camera"]
            obj_light = bpy.data.objects["Lamp"]
            obj_camera.data.type = "ORTHO"
            obj_camera.data.ortho_scale = domain*(11.0/3)
            obj_other = bpy.data.objects["BoundBOX"]
            look_at([obj_camera,obj_light],obj_other.location,loc)


class _2Dproject():
    
    def __init__(self,domain):
        
        try:
            bpy.data.objects['PLANE'].select = True
            bpy.context.scene.objects.unlink(bpy.data.objects['2Dcutting'])
            bpy.ops.object.delete() 
        except KeyError:
            pass
        bpy.ops.mesh.primitive_plane_add()
        self.plane = bpy.context.scene.objects.active
        #self.plane.location = (0, 0, domain*(2*random.random() -1))
        self.plane.location = (0, 0, random.gauss(0,domain*0.2))
        self.plane.scale=domain*Vector((1,1,1))
        mat = bpy.data.materials.get("planemat")
        if not mat:
            mat = bpy.data.materials.new("planemat")
            bpy.data.materials["planemat"].diffuse_color=[0,0,0]
        
        self.plane.active_material= mat
                
    def intersect(self,spheres):
        
        for sphere in spheres:
            bool = self.plane.modifiers.new(type="BOOLEAN",name="hatef")
            bool.object = sphere
            bool.operation = 'DIFFERENCE'
            sphere.hide_render = True
            
           

def runOperation(domain,scale,n):
    
    volfrac=[]
    for i in range(n):
    
        a=RandomSpheres(domain,scale)
        CamLight("2D",domain)
        a.PopulateDomain()
        a.SphereAdjust()
        b=_2Dproject(domain)
        b.intersect(a.returnSpheres())
        volfrac.append(a.VolumeFraction())
        name = "/home/hatef/Desktop/PhD/Phase_01_imageProcessing/Test/pics/img"+str(i)
        bpy.ops.render.render()
        bpy.data.images['Render Result'].save_render(name)
        print(str(100*i/float(n)) +"%")


    filename= "/home/hatef/Desktop/PhD/Phase_01_imageProcessing/Test/pics/volfrac"
    with open(filename, 'w') as f:
        for s in volfrac:
            f.write(str(s) + '\n')    
    print("100%")
    print("Operation complete.")    
    

runOperation(2,[1,1],2)
