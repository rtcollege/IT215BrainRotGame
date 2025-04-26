
class BallSimulation:
  """Handles ball physics simulation"""
  def __init__(self, display_surface, sX, sY):
      self.display_surface = display_surface
      self.data = Data(None)  # Initialize with None since we don't need UI reference
      self.balls = []
      self.circles = []
      self.circle_base_radius = 200
      self.ball_base_radius = 6
      self.base_padding = 100
      self.base_box_width = self.circle_base_radius * 2 + self.base_padding
      self.base_box_height = self.circle_base_radius * 2 + self.base_padding
      self.base_box_x = 100
      self.cell_size = 50
      self.grid = {}
      self.level = 1
      self.base_max_circles = 3  # Starting maximum number of circles
      self.base_ball_cost = 2
      self.can_spawn_circles = True
      self.spawn_timer = Timer(100, self.enable_circle_spawn)  # 1 second pause between levels
      self.health = 100
      self.min_radius_time = 0  # Track time at minimum radius
      self.base_damage = 1  # Base damage per second
      self.currency = 0
      self.last_stat_update = pygame.time.get_ticks()
      self.stat_update_delay = 1000  # 1 second in milliseconds

      self.spawn_button = Button(None, (0, 0), "Spawn Ball", 
                               pygame.font.Font(None, 24), "white", "#b68f40")

      # Initialize upgrade buttons
      self.multi_ball_button = Button(None, (0, 0), "Multi-Ball", 
                                    pygame.font.Font(None, 24), "white", "#b68f40")
      self.shrink_reduction_button = Button(None, (0, 0), "Shrink Reduction", 
                                          pygame.font.Font(None, 24), "white", "#b68f40")
      self.rotation_reduction_button = Button(None, (0, 0), "Rotation Reduction", 
                                            pygame.font.Font(None, 24), "white", "#b68f40")
      self.health_regen_button = Button(None, (0, 0), "Health Regen", 
                                      pygame.font.Font(None, 24), "white", "#b68f40")

      self.recalculate_layout(sX, sY)
      self.add_circle(sX, sY)

      self.angle_cache = {angle: (cos(radians(angle)), sin(radians(angle))) 
                         for angle in range(360)}
      self.spawn_pressed = False
      self.circle_pressed = False

  def recalculate_layout(self, sX, sY):
      """Recalculate simulation layout"""
      scale_factor = min(sX, sY)
      self.radius = int(self.circle_base_radius * scale_factor)
      self.box_width = int(self.base_box_width * sX)
      self.box_height = int(self.base_box_height * sY)
      self.box_x = int(self.base_box_x * sX)
      self.box_y = (self.display_surface.get_height() - self.box_height) // 2
      self.center_x = self.box_x + self.box_width // 2
      self.center_y = self.box_y + self.box_height // 2
      self.line_thickness = max(1, int(6 * scale_factor))

      # Rescale all circles
      for circle in self.circles:
          # Scale radius directly from base radius
          new_initial = int(self.circle_base_radius * scale_factor)
          ratio = circle.radius / circle.initial_radius
          circle.radius = int(new_initial * ratio)
          circle.initial_radius = new_initial
          circle.min_radius = int(20 * scale_factor)  # Scale minimum radius too
          circle.line_thickness = self.line_thickness
          circle.scale_factor = scale_factor

      # Rescale all balls
      for ball in self.balls:
          ball.rescale(self.center_x, self.center_y, scale_factor, self.ball_base_radius)

      self.font = pygame.font.Font("graphics/ui/NeotriadFree-1jzAg.ttf", 
                                 int(20 * scale_factor))
      # Position spawn button below circles
      button_y = self.box_y + self.box_height + int(30 * scale_factor)
      self.spawn_button.update_font(self.font)
      button_x = self.center_x - (self.spawn_button.rect.width // 2)
      self.spawn_button.set_position((button_x, button_y))

      # Position upgrade buttons on the right side
      upgrade_x = self.box_x + self.box_width + int(50 * scale_factor)
      upgrade_y = self.box_y
      upgrade_spacing = int(60 * scale_factor)

      for i, button in enumerate([self.multi_ball_button, self.shrink_reduction_button, 
                                self.rotation_reduction_button, self.health_regen_button]):
          button.update_font(self.font)
          button.set_position((upgrade_x, upgrade_y + i * upgrade_spacing))

  def get_current_ball_cost(self):
      return int(self.base_ball_cost * (1 + len(self.balls) * 0.2))  # 20% increase per ball

  def spawn_ball(self, sX, sY):
      scale_factor = min(sX, sY)
      ball_radius = self.ball_base_radius * scale_factor
      # Spawn multiple balls based on upgrade level
      for _ in range(1 + self.data.multi_ball_level):
          self.balls.append(Ball(self.center_x, self.center_y, ball_radius, self.center_x, self.center_y))

  def enable_circle_spawn(self):
      self.can_spawn_circles = True

  def add_circle(self, sX, sY):
      if not self.can_spawn_circles:
          return
      active_circles = sum(1 for c in self.circles if c.active)
      max_circles = self.base_max_circles + (self.level - 1)
      if active_circles >= max_circles:
          return

      scaled_radius = int(self.circle_base_radius * min(sX, sY))
      new_circle = Circle(scaled_radius, self.line_thickness)
      if not new_circle.check_collision(self.circles):
          self.circles.append(new_circle)
          return True
      return False

  def handle_collisions(self):
      for ball in self.balls[:]:
          dx = ball.x - self.center_x
          dy = ball.y - self.center_y
          dist = hypot(dx, dy)

          # Find all colliding circles
          colliding_circles = []
          for circle in self.circles:
              if not circle.active:
                  continue

              distance_to_ring = abs(dist - circle.radius)
              collision_margin = self.line_thickness + ball.radius

              if distance_to_ring <= collision_margin:
                  angle = (degrees(atan2(dy, dx)) + 360) % 360
                  if circle.is_in_gap(angle):
                      # Check if this is the only active circle
                      self.can_spawn_circles = False
                      self.spawn_timer.activate()
                      circle.active = False
                      # Award experience based on circle size
                      # Award experience and currency based on circle size
                      exp_gain = int((circle.initial_radius - circle.radius) / 2)
                      currency_gain = int((circle.initial_radius - circle.radius) / 4)  # Half of exp gain
                      self.data.experience += max(10, exp_gain)
                      self.currency += max(5, currency_gain)  # Minimum 5 currency
                      break
                  colliding_circles.append((circle, distance_to_ring, collision_margin))

          if not colliding_circles:
              continue

          # Handle collision with the nearest circle
          nearest_circle = min(colliding_circles, key=lambda x: x[1])
          circle, distance_to_ring, collision_margin = nearest_circle

          # Calculate normalized direction vectors
          norm_dx = dx / dist
          norm_dy = dy / dist

          # Calculate tangent vector (perpendicular to normal)
          tang_dx = -norm_dy
          tang_dy = norm_dx

          # Decompose velocity into normal and tangential components
          norm_vel = ball.vel_x * norm_dx + ball.vel_y * norm_dy
          tang_vel = ball.vel_x * tang_dx + ball.vel_y * tang_dy

          # Reflect normal component with bounce boost and minimal energy loss
          energy_loss = 0.995 - (0.02 * (len(colliding_circles) - 1))  # Less energy loss
          energy_loss = max(0.85, energy_loss)  # Higher minimum energy retention
          bounce_boost = 1.1  # Add extra energy on bounce
          norm_vel = -norm_vel * energy_loss * bounce_boost

          # Reconstruct velocity vector
          ball.vel_x = norm_vel * norm_dx + tang_vel * tang_dx
          ball.vel_y = norm_vel * norm_dy + tang_vel * tang_dy

          # Push ball out with increased push for multiple collisions
          penetration = collision_margin - distance_to_ring
          push_multiplier = 1 + (0.2 * (len(colliding_circles) - 1))  # Stronger push with more collisions
          if dist > circle.radius:  # Ball is outside ring
              ball.x -= norm_dx * (penetration + push_multiplier)
              ball.y -= norm_dy * (penetration + push_multiplier)
          else:  # Ball is inside ring
              ball.x += norm_dx * (penetration + push_multiplier)
              ball.y += norm_dy * (penetration + push_multiplier)

          # Clamp ball position to exactly the ring surface
          target_dist = circle.radius + (collision_margin if dist > circle.radius else -collision_margin)
          ball.x = self.center_x + norm_dx * target_dist
          ball.y = self.center_y + norm_dy * target_dist

          # Add minimal drag/friction
          drag = 0.995
          ball.vel_x *= drag
          ball.vel_y *= drag

  def update(self, dt, sX, sY):
      # Update level timer
      self.spawn_timer.update()

      # Apply health regeneration
      if self.health < 100:
          regen_amount = self.data.health_regen_level * 2 * dt  # 2 health per second per level
          self.health = min(100, self.health + regen_amount)

      # Update health and currency every second
      current_time = pygame.time.get_ticks()
      if current_time - self.last_stat_update >= self.stat_update_delay:
          # Update currency
          self.currency += 1

          # Check for minimum radius circles and update health with scaling damage
          has_min_radius = any(circle.active and circle.radius <= circle.min_radius for circle in self.circles)
          if has_min_radius:
              self.min_radius_time += self.stat_update_delay / 1000  # Convert to seconds
              damage = int(self.base_damage * (1 + self.min_radius_time / 5))  # Increase damage every 5 seconds
              self.health = max(0, self.health - damage)
          else:
              self.min_radius_time = 0  # Reset timer when no circles are at minimum radius

          self.last_stat_update = current_time

      # Draw status text
      status_x = int(20 * sX)
      status_y = int(20 * sY)
      spacing = int(40 * sY)

      health_text = self.font.render(f"Health: {self.health}", True, "white")
      currency_text = self.font.render(f"Currency: {self.currency}", True, "white")

      self.display_surface.blit(health_text, (status_x, status_y))
      self.display_surface.blit(currency_text, (status_x, status_y + spacing))

      # Draw level text within exp bar
      # Update and draw circles
      active_circles = [c for c in self.circles if c.active]
      if len(active_circles) == 0:
          if not self.circles:  # No circles at all
              if self.can_spawn_circles:
                  max_circles = self.base_max_circles + (self.level - 1)
                  for _ in range(max_circles):
                      self.add_circle(sX, sY)
              else:  # Had circles but all were destroyed
                  self.can_spawn_circles = False
                  self.spawn_timer.activate()
                  self.circles.clear()

      for circle in self.circles:
          circle.update(dt, self.circles, self.level)  # Pass level to circle update
          circle.draw(self.display_surface, self.center_x, self.center_y,
                      self.line_thickness, (182, 143, 64), pygame.gfxdraw)

      for ball in self.balls:
          ball.update(dt)

      self.handle_collisions()

      for ball in self.balls[:]:
          # Remove balls that hit the ground or outer ring
          if ball.y > self.display_surface.get_height():
              self.balls.remove(ball)
              # Refund half of the current ball cost
              refund = self.get_current_ball_cost() // 2
              self.currency += refund
          else:
              ball.draw(self.display_surface)

      self.add_circle(sX, sY)

      # Button UI
      self.spawn_button.update(self.display_surface)
      mouse_pos = pygame.mouse.get_pos()
      self.spawn_button.change_color(mouse_pos)
      if pygame.mouse.get_pressed()[0]:
          if self.spawn_button.check_input(mouse_pos) and not self.spawn_pressed:
              ball_cost = self.get_current_ball_cost()
              if self.currency >= ball_cost:
                  self.spawn_ball(sX, sY)
                  self.currency -= ball_cost
                  self.spawn_pressed = True
      else:
          self.spawn_pressed = False
          self.circle_pressed = False

      # Handle upgrade buttons
      upgrade_buttons = [
          (self.multi_ball_button, '_multi_ball_level'),
          (self.shrink_reduction_button, '_shrink_reduction_level'),
          (self.rotation_reduction_button, '_rotation_reduction_level'),
          (self.health_regen_button, '_health_regen_level')
      ]

      for button, attr in upgrade_buttons:
          # Get current level and cost
          current_level = getattr(self.data, attr)
          cost = self.data.get_upgrade_cost(current_level)

          # Update button text with cost
          button.text_input = f"{button.text_input.split(':')[0]}: {cost}"
          button.text = button.font.render(button.text_input, True, button.base_color)
          button.update(self.display_surface)
          button.change_color(mouse_pos)

          # Handle click
          if pygame.mouse.get_pressed()[0] and button.check_input(mouse_pos):
              if self.currency >= cost:
                  setattr(self.data, attr, current_level + 1)
                  self.currency -= cost