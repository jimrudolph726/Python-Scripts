    # def animate(self):
    #     # link is not moving
    #     if self.direction.x == 0 and self.direction.y == 0:
    #         self.frame_index = 0

    #         if self.attacking == True:
    #             if 'idle' in self.status:
    #                 self.status = self.status.replace('_idle','_attack')
    #             elif 'attack' in self.status:
    #                 self.status = self.status.replace('_attack','_attack')
    #             else:
    #                 self.status += '_attack'
    #         else:
    #             if 'idle' in self.status:
    #                 self.status = self.status.replace('_idle','_idle')
    #             elif 'attack' in self.status:
    #                 self.status = self.status.replace('_attack','_idle')
    #             else:
    #                 self.status += '_idle'

    #     if self.direction.x != 0 and self.direction.y != 0:
            
    #         if self.attacking == False:
    #             if 'idle' in self.status:
    #                 self.status = self.status.replace('_idle','')
    #             elif 'attack' in self.status:
    #                 self.status = self.status.replace('_attack','')
    #             else:
    #                 self.status += ''
    #         if self.attacking == True:
    #             if 'idle' in self.status:
    #                 self.status = self.status.replace('_idle','_attack')
    #             elif 'attack' in self.status:
    #                 self.status = self.status.replace('_attack','_attack')
    #             else:
    #                 self.status += '_attack'
        


    #     self.frame_index += 0.2
    #     if self.frame_index >= len(self.animations[self.status]):
    #         self.frame_index = 0
    #     self.image = self.animations[self.status][int(self.frame_index)]
    #     print(self.status)







    #     if self.direction.x == 0 and self.direction.y == 0:
    #         if '_idle' not in self.status: 
    #             if '_attack' not in self.status:
    #                 self.status += '_idle'
    #             else:
    #                 self.status = self.status.replace('_attack','_idle')
            
    #     if self.attacking == True:
    #         self.direction.x == 0
    #         self.direction.y == 0
    #         if '_attack' not in self.status:
    #             if '_idle' in self.status:
    #                 self.status = self.status.replace('_idle','_attack')
    #             else:
    #                 self.status += '_attack'